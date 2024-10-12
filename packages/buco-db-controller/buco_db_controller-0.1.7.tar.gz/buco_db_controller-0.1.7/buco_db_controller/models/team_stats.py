from datetime import datetime

from buco_db_controller.models.league import League
from buco_db_controller.models.team import Team


class TeamStats:
    def __init__(
            self,
            season,
            date,
            league,
            team,
            form,
            fixtures_played,
            fixtures_wins,
            fixtures_draws,
            fixtures_loses,

            goals_for,
            goals_against,

            biggest_streak,
            biggest_wins,
            biggest_loses,
            biggest_goals,

            clean_sheet,
            failed_to_score
    ):
        self.team = team
        self.league = league
        self.form = form
        self.fixtures_played = fixtures_played
        self.fixtures_wins = fixtures_wins
        self.fixtures_draws = fixtures_draws
        self.fixtures_loses = fixtures_loses
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.biggest_streak = biggest_streak
        self.biggest_wins = biggest_wins
        self.biggest_loses = biggest_loses
        self.biggest_goals = biggest_goals
        self.clean_sheet = clean_sheet
        self.failed_to_score = failed_to_score

    @classmethod
    def from_dict(cls, response):
        date = response['parameters']['date']
        season = response['parameters']['season']
        data = response['response']

        return cls(
            season=season,
            date=datetime.strptime(date, '%Y-%m-%d'),
            team=Team(
                team_id=data['team']['id'],
                name=data['team']['name'],
            ),
            league=League(
                league_id=data['league']['id'],
                name=data['league']['name']
            ),
            form=data['form'],
            fixtures_played=data['fixtures']['played'],
            fixtures_wins=data['fixtures']['wins'],
            fixtures_draws=data['fixtures']['draws'],
            fixtures_loses=data['fixtures']['loses'],
            goals_for=data['goals']['for'],
            goals_against=data['goals']['against'],
            biggest_streak=data['biggest']['streak'],
            biggest_wins=data['biggest']['wins'],
            biggest_loses=data['biggest']['loses'],
            biggest_goals=data['biggest']['goals'],
            clean_sheet=data['clean_sheet'],
            failed_to_score=data['failed_to_score']
        )
