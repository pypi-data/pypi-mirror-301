from buco_db_controller.models.team import Team


class XGoals:
    def __init__(
            self,
            fixture_id: str,
            date,

            home_team: Team,
            away_team: Team,

            home_xg,
            away_xg,

            home_goals,
            away_goals
    ):
        self.fixture_id = fixture_id
        self.date = date

        self.home_team = home_team
        self.away_team = away_team

        self.home_xg = home_xg
        self.away_xg = away_xg

        self.home_goals = home_goals
        self.away_goals = away_goals

    @classmethod
    def from_dict(cls, data):
        return cls(
            fixture_id=data['fixture']['id'],
            date=data['date'],

            home_team=Team(
                team_id=data['teams']['home']['id'],
                name=data['teams']['home']['name'],
            ),
            away_team=Team(
                team_id=data['teams']['away']['id'],
                name=data['teams']['away']['name'],
            ),

            home_xg=data['teams']['home']['xg'],
            away_xg=data['teams']['away']['xg'],

            home_goals=data['teams']['home']['goals'],
            away_goals=data['teams']['away']['goals']
        )
