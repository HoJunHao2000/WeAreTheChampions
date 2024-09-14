import os
import sys
import re

from managers.logging.ILoggingManager import ILoggingManager
from managers.logging.LoggingManager import LoggingManager
from managers.match.IMatchManager import IMatchManager
from managers.match.MatchManager import MatchManager
from managers.ranking.IRankingManager import IRankingManager
from managers.ranking.RankingManager import RankingManager
from managers.team.ITeamManager import ITeamManager
from managers.team.TeamManager import TeamManager

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
            '8': sys.exit
        }

        self._clear_terminal()

        while True:
            print("Options:\n")
            print("1. Input Teams")
            print("2. Input Matches")
            print("3. Display Rankings")
            print("4. Retrieve Team Details")
            print("5. Edit Team Data")
            print("6. Edit Match Data")
            print("7. Clear Data")
            print("8. Exit")

            choice = input("Enter choice: ")
            self._clear_terminal()
            action.get(choice, lambda: print("Please enter a number from 1 to 8."))()

    def _clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _input_teams(self):
        print("Enter team information (format: <Team name> <Registration date DD/MM> <Group number>):")
        while True:
            line = input()
            if line == '':
                break

            try:
                name, date, group = line.rsplit(' ', 2)
                group = int(group)
                if not re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])$", date):
                    raise ValueError
            except ValueError:
                print("Invalid format. Please enter in the format: <Team name> <Registration date DD/MM> <Group number>")
                continue

            if self.team_manager.team_exists(name):
                print(f"\nTeam '{name}' already exists.\n")
                continue
            self.team_manager.add_team(name, date, group)
            self.logging_manager.log(f"Added team '{name}' with registration date '{date}' and group number {group}.")

    def _input_matches(self):
        print("Enter match information (format: <Team A> <Team B> <Goals A> <Goals B>):")
        while True:
            line = input()
            if line == '':
                break

            try:
                team_a, team_b, goals_a, goals_b = line.rsplit(' ', 3)
                goals_a = int(goals_a)
                goals_b = int(goals_b)
            except ValueError:
                print("Invalid format. Please enter in the format: <Team A> <Team B> <Goals A> <Goals B>")
                continue

            if not self.team_manager.team_exists(team_a):
                print(f"\nTeam '{team_a}' does not exist.\n")
                self.logging_manager.log(f"Attempted to add match with non-existing team '{team_a}'.")
                continue
            if not self.team_manager.team_exists(team_b):
                print(f"\nTeam '{team_b}' does not exist.\n")
                self.logging_manager.log(f"Attempted to add match with non-existing team '{team_b}'.")
                continue
            self.match_manager.add_match(team_a, team_b, goals_a, goals_b)
            self.logging_manager.log(f"Added match between '{team_a}' and '{team_b}' with scores {goals_a}-{goals_b}.")

    def _display_rankings(self):
        while True:
            print("Rankings (Press Enter to exit):")
            matches = self.match_manager.all_matches()
            teams = self.team_manager.all_teams()
            rankings = self.ranking_manager.calculate_rankings(matches, teams)

            for group, ranked_teams in rankings.items():
                print(f"\nRankings for {group}:")
                for rank, team_info in enumerate(ranked_teams, start=1):
                    print(f"{rank}. {team_info['team']} - {team_info['total_points']} points, "
                          f"{team_info['total_goals']} goals, "
                          f"Registered: {team_info['registration_date']}")

            line = input("\nPress Enter to go back to the main menu or type anything to display rankings again: ")
            if line == '':
                break

    def _retrieve_team_details(self):
        print("Enter team name to retrieve details:")
        team_name = input()

        team_details = self.team_manager.retrieve_team(team_name)
        if team_details:
            print(f"Team: {team_name}")
            print(f"Date: {team_details['registration_date']}")
            print(f"Group: {team_details['group']}")

            all_matches = self.match_manager.all_matches()

            team_matches = [
                match for match in all_matches 
                if match['team_a'] == team_name or match['team_b'] == team_name
            ]

            print("Matches:")
            if team_matches:
                for match in team_matches:
                    opponent = match['team_b'] if match['team_a'] == team_name else match['team_a']
                    print(f"vs {opponent}: {match['goals_a']}-{match['goals_b']}")
            else:
                print("No matches found for this team.")
        else:
            print(f"Team '{team_name}' not found.")

    def _edit_team(self):
        print("Enter team information (format: <Old team name> <New team name> <Registration date DD/MM> <Group number>):")
        while True:
            line = input()
            if line == '':
                break

            try:
                old_name, name, date, group = line.rsplit(' ', 3)
                group = int(group)
                if not re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])$", date):
                    raise ValueError
            except ValueError:
                print("Invalid format. Please enter in the format: <Old team name> <New team name> <Registration date DD/MM> <Group number>")
                continue

            if not self.team_manager.team_exists(old_name):
                print(f"\nTeam '{old_name}' does not exist.\n")
                self.logging_manager.log(f"Attempted to edit non-existing team '{old_name}'.")
                continue
            self.team_manager.edit_team(old_name, name, date, group)
            self.logging_manager.log(f"Edited team '{old_name}' to new name '{name}', registration date '{date}', and group number {group}.")

    def _edit_match(self):
        print("Enter match information (format: <Match ID> <Team A> <Team B> <Goals A> <Goals B>):")
        while True:
            line = input()
            if line == '':
                break

            try:
                match_id, team_a, team_b, goals_a, goals_b = line.rsplit(' ', 4)
                match_id = int(match_id)
                goals_a = int(goals_a)
                goals_b = int(goals_b)
            except ValueError:
                print("Invalid format. Please enter in the format: <Match ID> <Team A> <Team B> <Goals A> <Goals B>")
                continue

            if not self.match_manager.match_exists(match_id):
                print(f"\nMatch ID '{match_id}' does not exist.\n")
                self.logging_manager.log(f"Attempted to edit non-existing match ID '{match_id}'.")
                continue
            self.match_manager.edit_match(match_id, team_a, team_b, goals_a, goals_b)
            self.logging_manager.log(f"Edited match ID '{match_id}' with new details: '{team_a}' vs '{team_b}' with scores {goals_a}-{goals_b}.")

    def _clear_data(self):
        self.team_manager.delete_all_teams()
        self.match_manager.delete_all_matches()
        print("All data cleared.")
        self.logging_manager.log("Cleared all teams and matches data.")


if __name__ == "__main__":
    teamManager = TeamManager()
    matchManager = MatchManager()
    rankingManager = RankingManager()
    loggingManager = LoggingManager()

    app = TournamentApp(teamManager, matchManager, rankingManager, loggingManager)
    app.main_menu()