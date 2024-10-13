from typing import Union, List

from buco_db_controller.models.team import Team
from buco_db_controller.models.team_stats import TeamStats
from buco_db_controller.repositories.fixture_repository import FixtureRepository
from buco_db_controller.repositories.team_repository import TeamRepository


class TeamService:
    def __init__(self):
        self.team_repository = TeamRepository()
        self.fixture_repository = FixtureRepository()

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

    def get_years_in_league(self, team_id: int, league_id: int, season: int) -> List[int]:
        previous_seasons = list(range(2014, season + 1))
        previous_leagues = []

        for season in previous_seasons:
            fixtures = self.fixture_repository.get_team_fixtures(team_id, league_id, season)

            if fixtures:
                league_id = fixtures[0]['league']['id']
            else:
                league_id = None

            previous_leagues.append(league_id)

        years_in_league_in_row = 0

        for previous_league_id in previous_leagues:
            if previous_league_id == league_id:
                years_in_league_in_row += 1
            else:
                years_in_league_in_row = 0

        return years_in_league_in_row
