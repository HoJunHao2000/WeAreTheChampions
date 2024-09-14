from abc import ABC, abstractmethod

class ITeamManager(ABC):
    @abstractmethod
    def add_team(self, name: str, date: str, group: int):
        pass

    @abstractmethod
    def all_teams(self) -> list:
        pass

    @abstractmethod
    def edit_team(self, old_name: str, name: str, date: str, group: int):
        pass

    @abstractmethod
    def team_exists(self, name: str) -> bool:
        pass

    @abstractmethod
    def is_same_group(self, name1: str, name2: str) -> bool:
        pass

    @abstractmethod
    def delete_all_teams(self):
        pass