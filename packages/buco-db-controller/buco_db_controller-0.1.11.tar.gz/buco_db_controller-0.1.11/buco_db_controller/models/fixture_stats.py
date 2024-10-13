

class FixtureStats:
    def __init__(
            self,
            fixture_id,
            home_fixture_stats,
            away_fixture_stats,
    ):
        self.fixture_id = fixture_id
        self.home_fixture_stats = home_fixture_stats
        self.away_fixture_stats = away_fixture_stats

    @classmethod
    def from_dict(cls, response):
        fixture_id = response['parameters']['fixture']

        home_fixture_stats = response['data'][0]
        away_fixture_stats = response['data'][1]

        return cls(
            fixture_id=fixture_id,
            home_fixture_stats=home_fixture_stats,
            away_fixture_stats=away_fixture_stats,
        )
