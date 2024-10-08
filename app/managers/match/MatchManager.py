import os
import requests
from requests.exceptions import RequestException
from managers.match.IMatchManager import IMatchManager

class MatchManager(IMatchManager):
    def __init__(self):
        self.match_service_url = os.getenv('MATCH_SERVICE_URL')
        if not self.match_service_url:
            raise ValueError("MATCH_SERVICE_URL environment variable not set")

    def add_match(self, team_a: str, team_b: str, goals_a: int, goals_b: int):
        """Adds a match by making a POST request to the match service API."""
        payload = {
            "team_a": team_a,
            "team_b": team_b,
            "goals_a": goals_a,
            "goals_b": goals_b
        }
        try:
            response = requests.post(f"{self.match_service_url}/matches", json=payload)
            response.raise_for_status()
        except RequestException as e:
            print(f"Failed to add match between '{team_a}' and '{team_b}'. Error: {e}")

    def all_matches(self) -> list:
        """Retrieves all matches by making a GET request to the match service API."""
        try:
            response = requests.get(f"{self.match_service_url}/matches")
            response.raise_for_status()  # Raise error for bad responses
            return response.json()  # Assuming the API returns the matches in JSON format
        except RequestException as e:
            print(f"Failed to retrieve matches. Error: {e}")
            return []
        
    def match_already_exists(self, team_a: str, team_b: str) -> bool:
        """Checks if a match between two teams already exists by making a GET request to the match service API."""
        try:
            response = requests.get(f"{self.match_service_url}/matches/{team_a}/{team_b}")
            response.raise_for_status()
            return len(response.json()) > 0
        except RequestException as e:
            return False

    def edit_match(self, match_id: int, team_a: str, team_b: str, goals_a: int, goals_b: int):
        """Edits an existing match by making a PUT request to the match service API."""
        payload = {
            "team_a": team_a,
            "team_b": team_b,
            "goals_a": goals_a,
            "goals_b": goals_b
        }
        try:
            response = requests.put(f"{self.match_service_url}/matches/{match_id}", json=payload)
            response.raise_for_status()
            print(f"Match {match_id} updated successfully.")
        except RequestException as e:
            print(f"Failed to update match {match_id}. Error: {e}")
    
    def match_exists(self, match_id: int) -> bool:
        """Checks if a match exists by making a GET request to the match service API."""
        try:
            response = requests.get(f"{self.match_service_url}/matches/{match_id}")
            return response.status_code == 200
        except RequestException as e:
            return False

    def delete_all_matches(self):
        """Deletes all matches by making a DELETE request to the match service API."""
        try:
            response = requests.delete(f"{self.match_service_url}/matches")
            response.raise_for_status()
            print("All matches deleted successfully.")
        except RequestException as e:
            print(f"Failed to delete all matches. Error: {e}")