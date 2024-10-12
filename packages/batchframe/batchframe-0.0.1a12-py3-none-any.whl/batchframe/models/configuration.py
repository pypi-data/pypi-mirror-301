from dataclasses import dataclass, field
from kink import inject
from datetime import datetime
from batchframe.models.batchframe_param import BatchframeParam

@inject
@dataclass()
class Configuration:
    """Base configuration class for batchframe.
    
    The underlined properties are auto-injected by the runtime. We call these static parameters.
    These should not be overriden in classes that inherit this one or pe provided in the CLI parameters.
        
    """
    _output_directory: str = field()
    _current_run_start: datetime
    _current_run_output_dir: str

    # Max number of items in the work buffer
    executor_work_queue_size: BatchframeParam[int] = 10

    # Number of workers in the producer-consumer pattern
    executor_consumers: BatchframeParam[int] = 3

    # Max nr. of retries for exceptions which trigger a retry (see _exceptions_to_retry_for in Service)
    executor_max_retries: BatchframeParam[int] = 3

    # List of time in seconds the executor should wait for before retrying,
    # starting from one retry and finishing with executor_max_retries
    executor_backoff_times_sec: list[float] = field(default_factory= lambda: [1,2,3])