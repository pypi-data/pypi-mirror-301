from buco_db_controller.models.team import Team


class TeamFixtureStats:
    def __init__(
            self,
            team,

            shots_on_goal,
            shots_off_goal,
            total_shots,
            blocked_shots,
            shots_insidebox,
            shots_outsidebox,
            fouls,
            corner_kicks,
            offsides,
            ball_possession,
            yellow_cards,
            red_cards,
            goalkeeper_saves,
            total_passes,
            pass_accuracy,
            passes,
    ):
        self.team = team

        self.shots_on_goal = shots_on_goal
        self.shots_off_goal = shots_off_goal
        self.total_shots = total_shots
        self.blocked_shots = blocked_shots
        self.shots_insidebox = shots_insidebox
        self.shots_outsidebox = shots_outsidebox
        self.fouls = fouls
        self.corner_kicks = corner_kicks
        self.offsides = offsides
        self.ball_possession = ball_possession  # Percentage
        self.yellow_cards = yellow_cards
        self.red_cards = red_cards
        self.goalkeeper_saves = goalkeeper_saves
        self.total_passes = total_passes
        self.pass_accuracy = pass_accuracy
        self.passes = passes  # Percentage

    @classmethod
    def from_dict(cls, response):
        data = TeamFixtureStats.convert_statistics_to_dict(response)

        return cls(
            team=Team(
                team_id=data['team']['id'],
                name=data['team']['name'],
            ),
            shots_on_goal=data['statistics']['Shots on Goal'],
            shots_off_goal=data['statistics']['Shots off Goal'],
            total_shots=data['statistics']['Total Shots'],
            blocked_shots=data['statistics']['Blocked Shots'],
            shots_insidebox=data['statistics']['Shots insidebox'],
            shots_outsidebox=data['statistics']['Shots outsidebox'],
            fouls=data['statistics']['Fouls'],
            corner_kicks=data['statistics']['Corner Kicks'],
            offsides=data['statistics']['Offsides'],
            ball_possession=data['statistics']['Ball Possession'],
            yellow_cards=data['statistics']['Yellow Cards'],
            red_cards=data['statistics']['Red Cards'],
            goalkeeper_saves=data['statistics']['Goalkeeper Saves'],
            total_passes=data['statistics']['Total passes'],
            pass_accuracy=data['statistics']['Passes accurate'],
            passes=data['statistics']['Passes %'],
        )

    @staticmethod
    def convert_statistics_to_dict(data):
        # Convert the JSON structure to a more accessible dictionary format
        data['statistics'] = {
            stat['type']: stat['value'] for stat in data['statistics']
        }
        return data
