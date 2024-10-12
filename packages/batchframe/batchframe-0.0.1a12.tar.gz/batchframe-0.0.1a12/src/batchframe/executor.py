from kink import inject
from batchframe.models.service import Service
from batchframe.models.configuration import Configuration
from batchframe.visuals import ProgressIndicator
from inspect import iscoroutinefunction
from asyncio import Queue, gather, get_event_loop, create_task, sleep, CancelledError, Task
from typing import Any
from dataclasses import dataclass
from IPython.terminal import embed as shell
import logging
import aiorwlock
import signal
import sys, os

_logger = logging.getLogger(__name__)

if sys.platform.lower() == "win32": os.system('') # Apparently enables terminal colors on windows

class PoisonPill:
    """Used to stop the workers from consuming from the queue.
    """
    pass

@dataclass(frozen=True, eq=False)
class WorkItem:
    item: Any
    retries: int = 0

    def __hash__(self) -> int:
        """This makes is hashable when wrapping non-hashable types.
        """
        return id(self)

@inject
class AsyncExecutor:

    _work_queue: Queue[WorkItem]
    _retry_work_queue: list[WorkItem]
    _service: Service
    _failed_work_inputs: list
    _items_to_process: int
    _items_processed: int
    _items_failed: int
    _items_worked_on: set[WorkItem]
    _num_consumers: int
    _lock: aiorwlock.RWLock
    _interruptable_tasks: set[Task]
    _exceptions_to_retry_for: set[type[Exception]]
    _max_retries: int
    _backoff_times_sec: list[float]
    _progress_indicator: ProgressIndicator
    _fill_work_queue: bool

    def __init__(
            self,
            service: Service,
            config: Configuration,
    ) -> None:
        _logger.debug('Async executor initiating!')
        
        self._work_queue = Queue(config.executor_work_queue_size)
        self._retry_work_queue = list()
        self._service = service
        self._failed_work_inputs = list()
        self._items_to_process = len(service.source)
        self._items_processed = 0
        self._items_failed = 0
        self._items_worked_on = set()
        self._num_consumers = config.executor_consumers
        self._interruptable_tasks = set()
        self._exceptions_to_retry_for = service.exceptions_to_retry_for
        self._max_retries = config.executor_max_retries
        self._progress_indicator = ProgressIndicator(self._items_to_process)
        self._fill_work_queue = True
        self._lock = aiorwlock.RWLock(fast=True)

        if len(config.executor_backoff_times_sec) == self._max_retries:
            self._backoff_times_sec = config.executor_backoff_times_sec
        elif self._max_retries == 0:
            logging.debug("Retry logic turned off!")
        else:
            raise ValueError('backoff_times_sec must have the same number of entries as max_retries!')

    def _register_signal_handlers(self):
        loop = get_event_loop()
        loop.add_signal_handler(signal.SIGINT, lambda signum=signal.SIGINT: create_task(self.pause_and_spawn_shell(signum)))

    def _spawn_shell(self, emergency: bool):
        self._progress_indicator.stop()
        header_text = "\033[34mBATCHFRAME PAUSE SHELL.\033[0m"
        if emergency:
            header_text = "\033[31mBATCHFRAME EMERGENCY SHELL\033[0m\nSystem is in an unstable state. Salvage what you can or simply let it crash!"
        shell.embed(header=f"{header_text}\n\nUse `self` object to control execution.", colors='neutral')
        # Needed because shell resets the handler
        self._register_signal_handlers()
        self._progress_indicator.start()

    async def pause_and_spawn_shell(self, signum):
        _logger.info("Trying to spawn shell...")
        if len(self._interruptable_tasks) > 0:
            for task in self._interruptable_tasks:
                if not task.cancelled():
                    task.cancel()
        
        async with self._lock.writer_lock:
            _logger.warning("Pausing and spawning shell...")
            self._spawn_shell(False)

    def _increment_items_processed(self) -> None:
        self._items_processed += 1
        self._progress_indicator.increment_succeeded()
        total_consumed = self._items_processed + self._items_failed
        logging.info(f'Processed item {self._items_processed} ({total_consumed}/{self._items_to_process})')

    def _increment_items_failed(self) -> None:
        self._items_failed += 1
        self._progress_indicator.increment_failed()
        total_consumed = self._items_processed + self._items_failed
        logging.warning(f'Failed processing item {self._items_failed} ({total_consumed}/{self._items_to_process})')

    async def _insert_into_work_queue(self, work_item: WorkItem):
        async with self._lock.reader:
            _logger.debug(f'Putting {work_item} into queue')
            try:
                await_task = create_task(self._work_queue.put(work_item))
                self._interruptable_tasks.add(await_task)
                await await_task
                self._interruptable_tasks.remove(await_task)
                _logger.debug(f'Put {work_item} into queue')
            except CancelledError:
                _logger.debug(f'Insertion into work queue cancelled, inserting {work_item} into retry queue instead.')
                self._retry_work_queue.append(work_item)

    def _drain_all_queues_into_failed(self):
        _logger.info("Putting all unfinished work items into the failed list.")
        
        while not self._work_queue.empty():
            work_item = self._work_queue.get_nowait().item
            if type(work_item) != PoisonPill:
                self._failed_work_inputs.append(work_item)

        self._failed_work_inputs.extend(self._service.source)
        
        while len(self._retry_work_queue) != 0:
            self._failed_work_inputs.append(self._retry_work_queue.pop().item)


    async def _fill_queue(self):
        while self._fill_work_queue:
            try:
                while len(self._retry_work_queue) != 0:
                    retry_input = self._retry_work_queue.pop()
                    await self._insert_into_work_queue(retry_input)
                work_input = self._service.source.next()
                work_item = WorkItem(work_input)
                await self._insert_into_work_queue(work_item)
            except StopIteration:
                break
            except Exception as e:
                _logger.debug('Iteration of source stopped with exception:', exc_info=e)
                raise e
        
        if not self._fill_work_queue:
            self._drain_all_queues_into_failed()

        while len(self._items_worked_on) != 0 or len(self._retry_work_queue) != 0 or not self._work_queue.empty():
            #_logger.debug("Cleaning up queues")
            #_logger.debug(f'{self._work_queue.qsize()=}')
            #_logger.debug(f'{len(self._retry_work_queue)=}')
            #_logger.debug(f'{len(self._items_worked_on)=}')
            #_logger.debug(f'{self._items_worked_on=}')
            if len(self._retry_work_queue) != 0:
                retry_input = self._retry_work_queue.pop()
                if self._fill_work_queue:
                    await self._insert_into_work_queue(retry_input)
                else:
                    self._failed_work_inputs.append(retry_input.item)
            
            await sleep(1)
        
        for _ in range(self._num_consumers):
                await self._work_queue.put(WorkItem(PoisonPill()))

        _logger.debug("Finished filling queue")

    async def _consume_work(self):
        while True:
            async with self._lock.reader_lock:       
                _logger.debug('Waiting for work...')  
                get_work_task = create_task(self._work_queue.get())
                self._interruptable_tasks.add(get_work_task)
                try:
                    work_input = await get_work_task
                except CancelledError:
                    continue
                finally:
                    self._interruptable_tasks.remove(get_work_task)
                _logger.debug(f'Got work input {work_input}')
                work_item = work_input.item
                retries_so_far = work_input.retries
                self._items_worked_on.add(work_input)

                if retries_so_far > 0:
                    sleep_time = self._backoff_times_sec[retries_so_far-1]
                    sleep_task = create_task(sleep(sleep_time))
                    self._interruptable_tasks.add(sleep_task)
                    try:
                        _logger.debug(f'Backing off for {sleep_time}s...')
                        await sleep_task
                    except CancelledError:
                        pass
                    self._interruptable_tasks.remove(sleep_task)

                if type(work_item) == PoisonPill:
                    _logger.debug('Stopping consumption.')
                    self._items_worked_on.remove(work_input)
                    break
                
                try:
                    if iscoroutinefunction(self._service.process):
                        await self._service.process(work_item)
                    else:
                        self._service.process(work_item)
                    self._increment_items_processed()
                except Exception as e:
                    logging.error(f'Caught error when processing {work_item}', exc_info=e)

                    if type(e) in self._exceptions_to_retry_for and retries_so_far < self._max_retries and self._fill_work_queue:
                        logging.debug(f'Putting {work_item} back in the retry queue')
                        self._retry_work_queue.append(WorkItem(work_item, retries_so_far+1))
                    else:
                        logging.debug(f'Putting {work_item} into list of failed inputs')
                        self._failed_work_inputs.append(work_item)
                        self._increment_items_failed()

                _logger.debug(f'Removing {work_item} from work list')
                self._items_worked_on.remove(work_input)

    def _call_finish_on_service(self):
        try:
            logging.debug("Calling service.finish()...")
            self._service.finish()
        except Exception as e:
            logging.error("Error occured during call to service.finish(). Starting interactive shell", exc_info=e)
            self._spawn_shell(True)

    def _persist_failed_items(self):
        if len(self._failed_work_inputs) > 0:
            try:
                logging.debug("Persisting failed work inputs")
                self._service.source.persist_failed(self._failed_work_inputs)
            except Exception as e:
                logging.error("Could not persist failed inputs. Starting interactive shell", exc_info=e)
                self._spawn_shell(True)

    def stop(self):
        _logger.info("Stopping execution! Please exit shell to finish process.")
        self._fill_work_queue = False

    async def execute(self):
        logging.info("Starting execution...")
        self._register_signal_handlers()

        consumers = [self._consume_work() for _ in range(self._num_consumers)]
        self._progress_indicator.start()
        try:
            await gather(self._fill_queue(), *consumers)
        except BaseException as e:
            _logger.error("Fatal error ocurred during execution!", exc_info=e)
            self._spawn_shell(True)
        _logger.debug("Starting cleanup tasks...")
        self._call_finish_on_service()
        self._persist_failed_items()
        self._progress_indicator.stop()
        logging.info("Finished execution")