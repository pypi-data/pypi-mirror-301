from typing import Union, List

from buco_db_controller.models.team import Team
from buco_db_controller.models.team_stats import TeamStats
from buco_db_controller.repositories.team_repository import TeamRepository


class TeamService:
    def __init__(self):
        self.team_repository = TeamRepository()

    def upsert_many_teams(self, teams: List[dict]):
        self.team_repository.upsert_many_teams(teams)

    def get_teams(self, league_id: int, season: int) -> List[Team]:
        response = self.team_repository.get_teams(league_id, season)

        if not response.get('data', []):
            raise ValueError(f'No teams found for league {league_id} and season {season}')

        teams = [Team.from_dict(team) for team in response['data']]
        return teams

    def get_team_ids(self, league_id: int, seasons: Union[int, List[int]]) -> List[int]:
        teams_over_seasons = self.team_repository.get_many_teams(league_id, seasons)

        team_ids = []
        for teams in teams_over_seasons:
            team_ids.extend([team['team']['id'] for team in teams['data']])

        team_ids = list(map(int, set(team_ids)))
        team_ids.sort()
        return team_ids
