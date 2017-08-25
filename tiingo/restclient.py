# -*- coding: utf-8 -*-
import requests
from requests.exceptions import HTTPError


class RestClientError(Exception):
    "Wrapper around HTTP Errors"
    pass


class RestClient(object):

    def __init__(self, config={}):
        """Base class for interacting with RESTful APIs

           Child class MUST have a ._base_url property!

            Args:
                config (dict): Arbitrary configuration options
        """
        self._config = config

        if config.get('session'):
            self._session = requests.Session()
        else:
            self._session = requests

    def __repr__(self):
        return '<RestClient(url="{}")>'.format(self._base_url)

    def _request(self, method, url, **kwargs):
        """Make HTTP request and return response object"""
        resp = self._session.request(method,
                                     '{}/{}'.format(self._base_url, url),
                                     headers=self._headers,
                                     **kwargs)

        try:
            resp.raise_for_status()
        except HTTPError as e:
            raise RestClientError(e)

        return resp
