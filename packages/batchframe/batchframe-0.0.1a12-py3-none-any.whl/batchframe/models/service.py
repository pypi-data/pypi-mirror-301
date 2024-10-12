from abc import ABCMeta, abstractmethod
from batchframe.models.source import Source
from typing import TypeVar, Generic

T = TypeVar('T')

class Service(Generic[T], metaclass=ABCMeta):

    source: Source[T]
    _exceptions_to_retry_for: set[type[Exception]]
    
    @property
    @abstractmethod
    def exceptions_to_retry_for(self) -> set[type[Exception]]:
        """If any of these exceptions are thrown by the process method,
        the retry logic will kick in and reschedule the failed input for future retries.

        Returns:
            set[type[Exception]]: Exceptions to retry for.
        """
        return self._exceptions_to_retry_for

    @abstractmethod
    def process(self, input: T):
        """Main method of a service.
        It will be called for each input from the source.
        An async version is supported.

        Args:
            input (T): Piece of work to process. Emitted by Source and injected by Executor.
        """
        pass

    @abstractmethod
    def finish(self):
        """Method called by Executor when the execution is finished, either properly or erroneously.

        This method allows you to do any extra work after processing, for example cleanup or persistence of some extra data.
        """
        pass