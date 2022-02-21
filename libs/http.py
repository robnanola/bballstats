"""
API consumer related base classes
"""

import json
import logging
import requests

from django.conf import settings
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text

logger = logging.getLogger(__name__)

class Response:
    """
    Consumer response class

    Parses and cleans http response content 
    """
    def __init__(self, response, status_code, url):
        """
        reponse : HTTP Response content
        status_code : HTTP status code
        url: HTTP Response URL
        """
        self._response = response
        self._status_code = status_code
        self._url = url

    def to_dict(self):
        """
        Converts json response to python dictionary
        """
        return json.loads(self._response)

    def is_valid(self):
        """
        Returns False if http status code is not 200 and
        json response is not valid
        """
        if self._status_code != 200:
            return False

        try:
            self.to_dict()
        except ValueError:
            return False
        return True

    def get_data_sets(self):
        """
        Cleans json response to a pandas dataframe compatible format
        """
        data = self.to_dict()
        if 'resultSets' in data:
            results = data['resultSets']
        else:
            results = data['resultSet']

        if isinstance(results, dict):
            if 'name' not in results:
                return {}
            return {
                results['name']: {
                    'headers': results['headers'],
                    'data': results['rowSet']
                }
            }

        return {
            result_set['name']: {
                'headers': result_set['headers'], 
                'data': result_set['rowSet']
            }
            for result_set in results
        }


class Request:
    """
    Consumer API Request class
    """
    base_url = 'https://stats.nba.com/stats/{endpoint}'
    
    def get(self, endpoint, parameters):
        """
        endpoint : API endpoint that will be appended to the base_url
        parameters : request parameters

        Executes the http GET request
        """
        base_url = self.base_url.format(endpoint=endpoint)
        endpoint = endpoint.lower()
        self.parameters = parameters

        response = requests.get(url=base_url, params=parameters, timeout=30)
        
        url = response.url
        status_code = response.status_code
        contents = response.text

        logger.info("REQUESTED URL: {}".format(response.url))
        logger.info("STATUS: {}".format(status_code))
        response_data = Response(response=contents, status_code=status_code, url=url)

        if response_data.is_valid() is False:
            raise Exception('Invalid response.')

        return response_data


class Endpoint:
    def create_db_engine(self):
        """
        Creates database connection via SQLAlchemy, since pandas dont have
        support for Django ORM.
        """
        return create_engine(
            "mysql+mysqldb://{user}:{password}@{host}/{name}?charset=utf8mb4".format(
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                host=settings.DATABASES['default']['HOST'],
                name=settings.DATABASES['default']['NAME']
            )
        )

    def truncate_table(self, engine, model):
        """
        Faster way of deleting all rows of a table. Though we can use the 
        django.db.connection.cursor, since we already have the SQLAlchemy 
        connection engine we can just reuse it.
        """
        logger.info('Deleting old rows.')
        connection = engine.connect()
        truncate_query = sa_text("TRUNCATE TABLE " + model._meta.db_table)
        connection.execution_options(autocommit=True).execute(truncate_query)
        logger.info('Old rows deleted.')

    def save_response(self):
        """
        This method need to be overriden when inheriting this class as 
        saving the response is always different for each endpoint
        """
        raise NotImplementedError('Need to override this method.')


class DataSet:
    key = None
    data = {}

    def __init__(self, data):
        """
        data: dictionary of data to be converted to a pandas Dataframe
        """
        self.data = data

    def _format_headers(self, headers):
        """
        headers: list of headers

        by default it convert it to lowercase
        """
        return list(map(lambda x: x.lower(), headers))

    def get_data_frame(self):
        """
        Converts data to pandas DataFrame
        """
        return DataFrame(
            self.data['data'],
            columns=self._format_headers(self.data['headers'])
        )
