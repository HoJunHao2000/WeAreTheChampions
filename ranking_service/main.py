from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from datetime import datetime

app = FastAPI()

# Helper function to parse date strings
def parse_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%d/%m")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}")

# Helper function to validate and parse input data
def validate_team_data(data: dict) -> dict:
    if not all(key in data for key in ("name", "date", "group")):
        raise ValueError("Missing required team fields")
    return {
        "name": str(data["name"]),
        "date":  parse_date(data["date"]),
        "group": int(data["group"])
    }

def validate_match_data(data: dict) -> dict:
    if not all(key in data for key in ("team_a", "team_b", "goals_a", "goals_b", "id")):
        raise ValueError("Missing required match fields")
    return {
        "team_a": str(data["team_a"]),
        "team_b": str(data["team_b"]),
        "goals_a": int(data["goals_a"]),
        "goals_b": int(data["goals_b"]),
        "id": int(data["id"])
    }

def calculate_rankings(teams: List[Dict[str, Any]], matches: List[Dict[str, Any]]) -> Dict[int, List[Dict[str, Any]]]:
    # Initialize ranking information for each team
    rankings = {}
    for team in teams:
        group = team["group"]
        if group not in rankings:
            rankings[group] = {}
        rankings[group][team["name"]] = {
            'total_points': 0,
            'total_goals': 0,
            'alternate_points': 0,
            'registration_date': team["date"],
        }

    # Process each match and update rankings
    for match in matches:
        team_a = match["team_a"]
        team_b = match["team_b"]
        goals_a = match["goals_a"]
        goals_b = match["goals_b"]

        # Find the group that both teams belong to (assuming they are in the same group)
        group_a = next((team["group"] for team in teams if team["name"] == team_a), None)
        group_b = next((team["group"] for team in teams if team["name"] == team_b), None)

        if group_a != group_b or group_a is None:
            continue  # Skip matches if teams are not in the same group or if teams don't exist

        group = group_a  # Both teams are in the same group

        # Update goals scored
        rankings[group][team_a]['total_goals'] += goals_a
        rankings[group][team_b]['total_goals'] += goals_b

        # Determine match points and alternate points
        if goals_a > goals_b:
            rankings[group][team_a]['total_points'] += 3
            rankings[group][team_a]['alternate_points'] += 5
            rankings[group][team_b]['alternate_points'] += 1
        elif goals_b > goals_a:
            rankings[group][team_b]['total_points'] += 3
            rankings[group][team_b]['alternate_points'] += 5
            rankings[group][team_a]['alternate_points'] += 1
        else:
            rankings[group][team_a]['total_points'] += 1
            rankings[group][team_b]['total_points'] += 1
            rankings[group][team_a]['alternate_points'] += 3
            rankings[group][team_b]['alternate_points'] += 3

    # Group teams by their respective groups
    grouped_rankings = {}
    for team in teams:
        group = team["group"]
        if group not in grouped_rankings:
            grouped_rankings[group] = []
        if team["name"] in rankings[group]:
            data = rankings[group][team["name"]]
            grouped_rankings[group].append({'team': team["name"], **data})

    # Sort teams within each group by the criteria
    for group in grouped_rankings:
        sorted_rankings = sorted(
            grouped_rankings[group],
            key=lambda item: (
                -item['total_points'],
                -item['total_goals'],
                -item['alternate_points'],
                item['registration_date']
            )
        )
        grouped_rankings[group] = sorted_rankings

    return grouped_rankings

@app.post("/rankings")
def get_rankings(payload: Dict[str, Any]):
    try:
        # Validate and parse input data
        teams = [validate_team_data(team) for team in payload["teams"]]
        matches = [validate_match_data(match) for match in payload["matches"]]
        
        # Calculate rankings
        results = calculate_rankings(teams, matches)
        return results
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error calculating rankings: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
