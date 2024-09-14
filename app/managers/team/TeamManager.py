import os
import requests
from requests.exceptions import RequestException

from app.managers.team import ITeamManager

class TeamManager(ITeamManager):
    def __init__(self):
        self.team_service_url = os.getenv('TEAM_SERVICE_URL')
        if not self.team_service_url:
            raise ValueError("TEAM_SERVICE_URL environment variable not set")

    def add_team(self, name: str, date: str, group: int):
        """Adds a team by making a POST request to the team service API."""
        payload = {
            "name": name,
            "date": date,
            "group": group
        }
        try:
            response = requests.post(f"{self.team_service_url}/teams", json=payload)
            response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx, 5xx)
            print(f"Team '{name}' added successfully.")
        except RequestException as e:
            print(f"Failed to add team '{name}'. Error: {e}")

    def edit_team(self, old_name: str, name: str, date: str, group: int):
        """Edits team details by making a PUT request to the team service API."""
        payload = {
            "name": name,
            "date": date,
            "group": group
        }
        try:
            response = requests.put(f"{self.team_service_url}/teams/{old_name}", json=payload)
            response.raise_for_status()
            print(f"Team '{old_name}' updated to '{name}' successfully.")
        except RequestException as e:
            print(f"Failed to update team '{old_name}'. Error: {e}")

    def team_exists(self, name: str) -> bool:
        """Checks if a team exists by making a GET request to the team service API."""
        try:
            response = requests.get(f"{self.team_service_url}/teams/{name}")
            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                return False
        except RequestException as e:
            print(f"Error checking if team '{name}' exists: {e}")
        return False

    def is_same_group(self, name1: str, name2: str) -> bool:
        """Checks if two teams are in the same group by comparing their group info."""
        try:
            response1 = requests.get(f"{self.team_service_url}/teams/{name1}")
            response2 = requests.get(f"{self.team_service_url}/teams/{name2}")
            
            response1.raise_for_status()
            response2.raise_for_status()

            group1 = response1.json().get("group")
            group2 = response2.json().get("group")
            
            return group1 == group2
        except RequestException as e:
            print(f"Error comparing teams '{name1}' and '{name2}': {e}")
        return False

    def delete_all_teams(self):
        """Deletes all teams by making a DELETE request to the team service API."""
        try:
            response = requests.delete(f"{self.team_service_url}/teams")
            response.raise_for_status()
            print("All teams deleted successfully.")
        except RequestException as e:
            print(f"Failed to delete all teams. Error: {e}")
