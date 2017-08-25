# -*- coding: utf-8 -*-
import requests
from requests.exceptions import HTTPError


# TODO: Possibly print HTTP json response if available?
class RestClientError(Exception):
    "Wrapper around HTTP Errors"
    pass


class RestClient(object):

    def __init__(self, config={}):
        """Base class for interacting with RESTful APIs
           Child class MUST have a ._base_url property!

            Args:
                config (dict): Arbitrary options that child classes can access
        """
        self._config = config

        if config.get('session'):
            self._session = requests.Session()
        else:
            self._session = requests

    def __repr__(self):
        return '<RestClient(url="{}")>'.format(self._base_url)

    def _request(self, method, url, **kwargs):
        """Make HTTP request and return response object

            Args:
                method (str): GET, POST, PUT, DELETE
                url (str): path appended to the base_url to create request
                **kwargs: passed directly to a requests.request object
        """
        resp = self._session.request(method,
                                     '{}/{}'.format(self._base_url, url),
                                     headers=self._headers,
                                     **kwargs)

        try:
            resp.raise_for_status()
        except HTTPError as e:
            raise RestClientError(e)

        return resp
