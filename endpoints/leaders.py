"""
API Consumer Endpoint for LeaderBoards
"""
import logging
from datetime import date

from app.models import PlayerStatistic
from libs.http import Request, Endpoint, DataSet

logger = logging.getLogger(__name__)

def is_valid_season(season):
    """
    Validates if season has the correct format.
    """
    today = date.today()
    season = season.split('-')

    if season[0] and season[0].isdigit():
        if int(season[0]) >=1900 and int(season[0]) <= today.year + 1:
          if int(season[1]) - int(season[0][2:]) == 1:
            return True

    return False

class Leaders(Endpoint):
    """
    Consume the leagueleaders/ endpoints
    """
    endpoint = 'leagueleaders'

    def __init__(self, season='2021-22'):
        """
        Setup request parameters and execute the GET request
        """
        if is_valid_season(season) is False:
            raise Exception('Invalid season format (YYYY-YY); ie: 2019-20')

        self.parameters = {
                'LeagueID': '00',
                'PerMode': 'Totals',
                'Scope': 'S',
                'Season': season,
                'SeasonType': 'Regular Season',
                'StatCategory': 'PTS',
                # 'ActiveFlag': ''
        }

        self.response = Request().get(
            endpoint=self.endpoint,
            parameters=self.parameters
        )


    def is_valid_season(self, season):
        """
        Validates if season has the correct format.
        """
        today = date.today()
        season = season.split('-')

        if season[0] and season[0].isdigit():
            if int(season[0]) >=1900 and int(season[0]) <= today.year + 1:
              if int(season[1]) - int(season[0][2:]) == 1:
                return True

        return False


    def save_response(self):
        """
        Process the endpoint response and save it into the database
        """
        logger.info('Processing response data..')
        data_sets = self.response.get_data_sets()
        league_leaders = DataSet(data=data_sets['LeagueLeaders'])

        # rename column name before saving as there is no 'min' column in our model
        dataframe = league_leaders.get_data_frame().rename(columns={'min': 'minutes'})
        db_engine = self.create_db_engine()

        # fastest way to delete all rows since we only need the updated data
        self.truncate_table(db_engine, PlayerStatistic)

        logger.info("Inserting new data...")

        # save dataframe to the model, 
        # this is a limitation of pandas DataFrame.to_sql support for 
        # Django ORM. we will use SQLAlchemy instead.
        dataframe.to_sql(
            PlayerStatistic._meta.db_table,
            self.create_db_engine(),
            if_exists='append',
            index=False
        )
        logger.info("Done.")
