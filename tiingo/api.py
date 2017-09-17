# -*- coding: utf-8 -*-

import os
import sys
import pkg_resources
import csv
from zipfile import ZipFile


from tiingo.restclient import RestClient
import requests

VERSION = pkg_resources.get_distribution("tiingo").version


# These methods enable python 2 + 3 compatibility.
def get_zipfile_from_response(response):
    if sys.version_info < (3, 0):  # python 2
        from StringIO import StringIO as Buffer
    else:  # python 3
        from io import BytesIO as Buffer
    buffered = Buffer(response.content)
    return ZipFile(buffered)


def get_buffer_from_zipfile(zipfile, filename):
    if sys.version_info < (3, 0):  # python 2
        from StringIO import StringIO
        return StringIO(zipfile.read(filename))
    else:  # python 3
        # Source:
        # https://stackoverflow.com/questions/5627954/py3k-how-do-you-read-a-file-inside-a-zip-file-as-text-not-bytes
        from io import (TextIOWrapper, BytesIO)
        return TextIOWrapper(BytesIO(zipfile.read(filename)))


class TiingoClient(RestClient):
    """Class for managing interactions with the Tiingo REST API

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
            'User-Agent': 'tiingo-python-client {}'.format(VERSION)
        }

    def __repr__(self):
        return '<TiingoClient(url="{}")>'.format(self._base_url)

    # TICKER PRICE ENDPOINTS
    # https://api.tiingo.com/docs/tiingo/daily
    def list_stock_tickers(self):
        """Return a list of dicts of metadata tickers for all supported Stocks
            as well as metadata about each ticker. This includes supported
            date range, the exchange the ticker is traded on, and the currency
            the stock is traded on.
           Tickers for unrelated products are omitted.
           https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip
           """
        listing_file_url = "https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip"
        response = requests.get(listing_file_url)
        zipdata = get_zipfile_from_response(response)
        raw_csv = get_buffer_from_zipfile(zipdata, 'supported_tickers.csv')
        reader = csv.DictReader(raw_csv)

        return [row for row in reader
                if row.get('assetType') == 'Stock']

    def get_ticker_metadata(self, ticker):
        """Return metadata for 1 ticker
           Use TiingoClient.list_tickers() to get available options

            Args:
                ticker (str) : Unique identifier for stock
        """
        url = "tiingo/daily/{}".format(ticker)
        response = self._request('GET', url)
        return response.json()

    def get_ticker_price(self, ticker,
                         startDate=None, endDate=None,
                         fmt='json', frequency='daily'):
        """By default, return latest EOD Composite Price for a stock ticker.
           On average, each feed contains 3 data sources.

            Supported tickers + Available Day Ranges are here:
            https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip

            Args:
                ticker (string): Unique identifier for stock ticker
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

        # TODO: evaluate whether to stream CSV to cache on disk, or
        # load as array in memory, or just pass plain text
        response = self._request('GET', url, params=params)
        if fmt == "json":
            return response.json()
        else:
            return response.content.decode("utf-8")

    # NEWS FEEDS
    # tiingo/news
    def get_news(self, tickers=[], tags=[], sources=[], startDate=None,
                 endDate=None, limit=100, offset=0, sortBy="publishedDate"):
        """Return list of news articles matching given search terms
            https://api.tiingo.com/docs/tiingo/news

            # Dates are in YYYY-MM-DD Format.

            Args:
                tickers [string] : List of unique Stock Tickers to search
                tags [string] : List of topics tagged by Tiingo Algorithms
                sources [string]: List of base urls to include as news sources
                startDate, endDate [date]: Boundaries of news search window
                limit (int): Max results returned. Default 100, max 1000
                offset (int): Search results offset, used for paginating
                sortBy (string): "publishedDate" OR (#TODO: UPDATE THIS)
        """
        url = "tiingo/news"
        params = {
            'limit': limit,
            'offset': offset,
            'sortBy': sortBy,
            'tickers': tickers,
            'sources': sources,
            'tags': tags,
            'startDate': startDate,
            'endDate': endDate
        }
        response = self._request('GET', url, params=params)
        return response.json()

    def get_bulk_news(self, file_id=None):
        """Only available to institutional clients.
            If ID is NOT provided, return array of available file_ids.
            If ID is provided, provides URL which you can use to download your
            file, as well as some metadata about that file.
        """
        if file_id:
            url = "tiingo/news/bulk_download/{}".format(file_id)
        else:
            url = "tiingo/news/bulk_download"

        response = self._request('GET', url)
        return response.json()
