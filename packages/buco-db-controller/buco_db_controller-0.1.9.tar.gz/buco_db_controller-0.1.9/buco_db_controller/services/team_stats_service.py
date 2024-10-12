from typing import List

from buco_db_controller.models.team_stats import TeamStats
from buco_db_controller.repositories.team_stats_repository import TeamStatsRepository


class TeamStatsService:
    def __init__(self):
        self.team_repository = TeamStatsRepository()

    def upsert_many_team_stats(self, team_stats: List[dict]):
        self.team_repository.upsert_many_team_stats(team_stats)

    def get_team_stats(self, team_id: int, league_id: int, season: int):
        response = self.team_repository.get_team_stats(team_id, league_id, season)

        if not response.get('data', []):
            raise ValueError(f'No team stats found for team {team_id}, league {league_id} and season {season}')

        team_stats = TeamStats.from_dict(response)
        return team_stats
