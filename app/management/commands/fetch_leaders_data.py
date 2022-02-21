"""
Custom management command for downloading NBA Leaders Data
"""

import logging

from django.core.management.base import BaseCommand, CommandError

from endpoints.leaders import Leaders

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

        try:
            if season:
                season_leaders = Leaders(season)
            else:
                season_leaders = Leaders()
        except Exception as err:
            logger.error("Data download failed.")
        
        season_leaders.save_response()


