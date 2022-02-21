"""
Custom management command for downloading NBA Leaders Data
"""

import logging

from django.core.management.base import BaseCommand, CommandError

from endpoints.leaders import Leaders, is_valid_season

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch data of the NBA season leaders and save it to the database.'

    def add_arguments(self, parser):
        """
        Add season optional argument
        """
        parser.add_argument('-s', '--season', type=str, help='NBA Season ie: 1996-97', )

    def handle(self, *args, **options):
        """
        Fetch and saves data.
        """
        logger.info('Fetching league leaders data...')
        season = options['season']

        season_leaders = None

        try:
            if season:
                if is_valid_season(season):
                    season_leaders = Leaders(season)
                else:
                    logger.info('Invalid season format (YYYY-YY); ie: 2019-20')
            else:
                season_leaders = Leaders()
        except Exception as err:
            logger.info("Data download failed.")
        
        if season_leaders:
            season_leaders.save_response()


