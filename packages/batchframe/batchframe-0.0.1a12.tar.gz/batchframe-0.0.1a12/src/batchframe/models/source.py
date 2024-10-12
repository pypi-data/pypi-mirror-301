from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class Source(Generic[T], metaclass=ABCMeta):
    """This class is essentially a Python iterator with extra functionality: https://wiki.python.org/moin/Iterator.

    Args:
        Generic (_type_): Type of output this source produces
    """
    
    def __iter__(self):
        return self
    
    def __next__(self) -> T:
        return self.next()
    
    @abstractmethod
    def __len__(self) -> int:
        """Returns the total number of items to be processed.

        Returns:
            int: Total number of items to be processed.
        """
        pass
    
    @abstractmethod
    def next(self) -> T:
        """Return the next item to be processed, or raise the StopIteration exception when there are none left.

        Returns:
            T: The next item to be processed.
        """
        pass

    @abstractmethod
    def persist_failed(self, failed: list[T]):
        """Method called by the executor with inputs that caused errors in the execution.
        Use this method to persist these inputs for analysis and future re-use.

        Args:
            failed (list[T]): Inputs produced by this source which could not be processed.
        """
        pass