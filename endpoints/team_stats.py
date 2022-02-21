from pandas import DataFrame

from app.models import PlayerStatistic
from libs.http import Request, Endpoint


class DataSet:    
    key = None
    data = {}

    def __init__(self, data):
        self.data = data

    def _format_headers(self, headers):
        return list(map(lambda x: x.lower(), headers))

    def get_data_frame(self):
        return DataFrame(self.data['data'], columns=self._format_headers(self.data['headers']))


class TeamStats(Endpoint):
    endpoint = 'leaguedashteamstats'

    def __init__(self):
        self.parameters = {
                'LastNGames': '0',
                'MeasureType': 'Base',
                'Month': '0',
                'OpponentTeamID': 0,
                'PaceAdjust': 'N',
                'PerMode': 'Totals',
                'Period': '0',
                'PlusMinus': 'N',
                'Rank': 'N',
                'Season': '2021-22',
                'SeasonType': 'Regular Season',
                'Conference': '',
                'DateFrom': '',
                'DateTo': '',
                'Division': '',
                'GameScope': '',
                'GameSegment': '',
                'LeagueID': '',
                'Location': '',
                'Outcome': '',
                'PORound': '',
                'PlayerExperience': '',
                'PlayerPosition': '',
                'SeasonSegment': '',
                'ShotClockRange': '',
                'StarterBench': '',
                'TeamID': '',
                'TwoWay': '',
                'VsConference': '',
                'VsDivision': ''
        }

        self.response = Request().get(
            endpoint=self.endpoint,
            parameters=self.parameters
        )

        data_sets = self.response.get_data_sets()

        self.team_stats = Endpoint.DataSet(data=data_sets['LeagueDashTeamStats'])
        self.team_stats.get_data_frame()
