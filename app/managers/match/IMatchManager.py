from abc import ABC, abstractmethod

class IMatchManager(ABC):
    @abstractmethod
    def add_match(self, team_a: str, team_b: str, goals_a: int, goals_b: int):
        pass

    @abstractmethod
    def all_matches(self) -> list:
        pass
    
    @abstractmethod
    def edit_match(self, match_id: int, team_a: str, team_b: str, goals_a: int, goals_b: int):
        pass

    @abstractmethod
    def delete_all_matches(self):
        pass