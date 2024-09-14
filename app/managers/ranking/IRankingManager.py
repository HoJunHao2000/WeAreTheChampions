from abc import ABC, abstractmethod

class IRankingManager(ABC):
    @abstractmethod
    def calculate_rankings(self, matches: list, teams: list) -> list:
        pass