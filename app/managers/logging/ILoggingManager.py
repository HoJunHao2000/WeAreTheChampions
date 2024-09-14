from abc import ABC, abstractmethod

class ILoggingManager(ABC):
    @abstractmethod
    def log(self, message: str):
        pass

    @abstractmethod
    def view_logs(self) -> list:
        pass