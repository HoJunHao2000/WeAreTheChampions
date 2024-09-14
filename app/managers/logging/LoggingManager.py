import os
import requests
from requests.exceptions import RequestException
from datetime import datetime

from app.managers.logging import ILoggingManager

class LoggingManager(ILoggingManager):
    def __init__(self):
        self.log_service_url = os.getenv('LOG_SERVICE_URL')
        if not self.log_service_url:
            raise ValueError("LOG_SERVICE_URL environment variable not set")
    
    def log(self, message: str):
        """Logs a message by making a POST request to the log service API."""
        payload = {
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        try:
            response = requests.post(f"{self.log_service_url}/logs", json=payload)
            response.raise_for_status()
            print("Log message added successfully.")
        except RequestException as e:
            print(f"Failed to log message. Error: {e}")
    
    def view_logs(self) -> list:
        """Retrieves all logs by making a GET request to the log service API."""
        try:
            response = requests.get(f"{self.log_service_url}/logs")
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Failed to retrieve logs. Error: {e}")
            return []