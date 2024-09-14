import os
import sys

from app.managers.logging import ILoggingManager, LoggingManager
from app.managers.team import ITeamManager, TeamManager
from app.managers.match import IMatchManager, MatchManager
from app.managers.ranking import IRankingManager, RankingManager

class TournamentApp:
    def __init__(
        self,
        team_manager: ITeamManager,
        match_manager: IMatchManager,
        ranking_manager: IRankingManager,
        logging_manager: ILoggingManager
    ):
        self.team_manager = team_manager
        self.match_manager = match_manager
        self.ranking_manager = ranking_manager
        self.logging_manager = logging_manager

    def main_menu(self):
        action = {
            '1': self._input_teams,
            '2': self._input_matches,
            '3': self._display_rankings,
            '4': self._retrieve_team_details,
            '5': self._edit_team,
            '6': self._edit_match,
            '7': self._clear_data,
            '8': sys.exit()
        }

        while True:
            self._clear_terminal()
            print("\nOptions:")
            print("1. Input Teams")
            print("2. Input Matches")
            print("3. Display Rankings")
            print("4. Retrieve Team Details")
            print("5. Edit Team Data")
            print("6. Edit Match Data")
            print("7. Clear Data")
            print("8. Exit")

            choice = input("Enter choice: ")
            action.get(choice, lambda: print("Please enter a number from 1 to 8."))()

    def _clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _input_teams(self):
        pass

    def _input_matches(self):
        pass

    def _display_rankings(self):
        pass

    def _retrieve_team_details(self):    
        pass

    def _edit_team(self):
        pass

    def _edit_match(self):
        pass

    def _clear_data(self):
        pass