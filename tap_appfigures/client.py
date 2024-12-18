"""
The AppFigures API client
"""

import sys

import requests

import singer

from tap_appfigures.utils import RequestError


LOGGER = singer.get_logger()


class AppFiguresClient:
    """
    The client
    """
    BASE_URI = "https://api.appfigures.com/v2/"

    def __init__(self, config):
        self.pat = config.get('pat')
        self.start_date = config.get('start_date')

    def make_request(self, uri):
        """
        Make a request to BASE_URI/uri
        and handle any errors
        """
        LOGGER.info("Making get request to {}".format(uri))
        headers = {"Authorization": f'Bearer {self.pat}'}
        try:
            response = requests.get(
                self.BASE_URI + uri.lstrip("/"),
                headers=headers
            )
        except Exception as e:
            LOGGER.error('Error [{}], request {} failed'.format(e, uri))
            raise RequestError

        if response.status_code == 420:
            LOGGER.critical('Daily rate limit reached, after request for {}'.format(uri))
            sys.exit(1)

        response.raise_for_status()
        return response
