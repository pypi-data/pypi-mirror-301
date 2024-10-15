from buco_db_controller.models.team import Team


class Odds:
    def __init__(
            self,
            fixture_id: int,
            date,

            home_team: Team,
            away_team: Team,

            result,
            over_under,
            btts,
            dnb,
    ):
        self.fixture_id = fixture_id
        self.date = date

        self.home_team = home_team
        self.away_team = away_team

        self.result = result
        self.over_under = over_under
        self.btts = btts
        self.dnb = dnb

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

            result=data['odds']['1X2'],
            over_under=data['odds']['over_under'],
            btts=data['odds']['btts'],
            dnb=data['odds']['dnb'],
        )
