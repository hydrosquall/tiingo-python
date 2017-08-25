# -*- coding: utf-8 -*-

import os
from tiingo.restclient import RestClient


class TiingoClient(RestClient):
    """Class for managing interactions with the Tiingo Platform

    Supply API Key via Environment Variable TIINGO_API_KEY
    or via the Config Object
    """

    def __init__(self, *args, **kwargs):
        super(TiingoClient, self).__init__(*args, **kwargs)
        self._base_url = "https://api.tiingo.com"

        try:
            api_key = self._config['api_key']
        except KeyError:
            api_key = os.environ.get('TIINGO_API_KEY')

        assert(api_key)

        self._headers = {
            'Authorization': "Token {}".format(api_key),
            'Content-Type': 'application/json',
            'User-Agent': 'tiingo-python-client'
        }

    def __repr__(self):
        return '<TiingoClient(url="{}")>'.format(self._base_url)

    # PRICE ENDPOINTS
    def get_ticker_metadata(self, ticker):
        """Return metadata for 1 ticker.
        """
        url = "tiingo/daily/{}".format(ticker)
        response = self._request('GET', url)
        return response.json()

    def get_ticker_price(self, ticker, startDate=None, endDate=None,
                         fmt='json',
                         frequency='daily'):
        """
            By default, return latest EOD Composite Price for a stock ticker.

            Each feed on average contains 3 data sources.

            Supported tickers + Available Day Ranges are here:
                https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip

            Args:
                startDate (string): Start of ticker range in YYYY-MM-DD format
                endDate (string): End of ticker range in YYYY-MM-DD format
                fmt (string): 'csv' or 'json'
                frequency (string): Resample frequency
        """

        url = "tiingo/daily/{}/prices".format(ticker)

        params = {
            'format': fmt,
            'frequency': frequency
        }

        if startDate:
            params['startDate'] = startDate
        if endDate:
            params['endDate'] = endDate

        response = self._request('GET', url, params=params)
        return response.json()
