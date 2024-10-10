

from abc import ABC, abstractmethod
#create abstract class BaseHandler
class BaseHandler(ABC):
    @abstractmethod
    def __call__(self, func):
        pass