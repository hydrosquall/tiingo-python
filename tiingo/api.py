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

    # TICKER PRICE ENDPOINTS
    # https://api.tiingo.com/docs/tiingo/daily
    def get_price_metadata(self, ticker):
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

    # FUND DATA (From over 26,000 mutual funds)
    # https://api.tiingo.com/docs/tiingo/funds
    # TODO: Validate the models returned by the fund
    def get_fund_metadata(self, fund):
        """Return metadata for 1 mutual fund / ETF
        """
        url = "tiingo/funds/{}".format(fund)
        response = self._request('GET', url)
        return response.json()

    def get_fund_metrics(self, fund, startDate=None, endDate=None):
        """Return metrics about a fund. By default, return latest metrics.
            Args:
                startDate (string): Start of fund range in YYYY-MM-DD format
                endDate (string): End of fund range in YYYY-MM-DD format
                fmt (string): 'csv' or 'json'
                frequency (string): Resample frequency
        """
        url = "tiingo/funds/{}/metrics".format(fund)
        params = {}
        if startDate:
            params['startDate'] = startDate
        if endDate:
            params['endDate'] = endDate

        response = self._request('GET', url, params=params)
        return response.json()

    # NEWS FEEDS
    def get_news(self, tickers=[], tags=[], sources=[], startDate=None,
                 endDate=None, limit=100, offset=0, sortBy="publishedDate"):
        """Return metrics about a fund. By default, return latest metrics.
            Args:
                startDate (string): Start of fund range in YYYY-MM-DD format
                endDate (string): End of fund range in YYYY-MM-DD format
                fmt (string): 'csv' or 'json'
                frequency (string): Resample frequency
        """
        # Stub:
        # https://api.tiingo.com/docs/tiingo/news
        # "Finish later"
        raise NotImplementedError

    def get_bulk_news(self, file_id=None):
        """Only available to institutional clients.
            If no ID is provided, return array of available ids.
            If ID is provided, provides URL which you can use to download your
            file, as well as some metadata about that file.
        """
        # Stub:
        # https://api.tiingo.com/docs/tiingo/news
        # "Finish later"
        if file_id:
            url = "tiingo/news/bulk_download"
        else:
            url = "tiingo/news/bulk_download{}".format(file_id)
        response = self._request('GET', url)
        return response.json()
