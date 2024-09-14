import os
import requests
from requests.exceptions import RequestException
from app.managers.ranking.IRankingManager import IRankingManager

class RankingManager(IRankingManager):
    def __init__(self):
        # Retrieve the ranking_service_url from environment variables
        self.ranking_service_url = os.getenv('RANKING_SERVICE_URL')
        if not self.ranking_service_url:
            raise ValueError("RANKING_SERVICE_URL environment variable not set")
        
    def calculate_rankings(self, matches: list, teams: list) -> list:
        """Calculates the rankings based on match results."""
        payload = {
            "matches": matches,
            "teams": teams
        }
        try:
            response = requests.post(f"{self.ranking_service_url}/rankings", json=payload)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Failed to calculate rankings. Error: {e}")
            return {}