# -*- coding: utf-8 -*-

from collections import namedtuple
import csv
import json
import os
import re
import sys
from zipfile import ZipFile

import requests

from tiingo.restclient import RestClient
from tiingo.exceptions import (
    InstallPandasException,
    APIColumnNameError,
    InvalidFrequencyError,
    MissingRequiredArgumentError,
)

from tiingo.__version__ import __version__ as VERSION

try:
    import pandas as pd

    pandas_is_installed = True
except ImportError:
    pandas_is_installed = False


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
        from io import TextIOWrapper, BytesIO

        return TextIOWrapper(BytesIO(zipfile.read(filename)))


def dict_to_object(item, object_name):
    """Converts a python dict to a namedtuple, saving memory."""
    fields = item.keys()
    values = item.values()
    return json.loads(
        json.dumps(item), object_hook=lambda d: namedtuple(object_name, fields)(*values)
    )


class TiingoClient(RestClient):
    """Class for managing interactions with the Tiingo REST API

    Supply API Key via Environment Variable TIINGO_API_KEY
    or via the Config Object
    """

    def __init__(self, *args, **kwargs):
        super(TiingoClient, self).__init__(*args, **kwargs)
        self._base_url = "https://api.tiingo.com"

        try:
            api_key = self._config["api_key"]
        except KeyError:
            api_key = os.environ.get("TIINGO_API_KEY")
        self._api_key = api_key

        if not (api_key):
            raise RuntimeError(
                "Tiingo API Key not provided. Please provide"
                " via environment variable or config argument."
            )

        self._headers = {
            "Authorization": "Token {}".format(api_key),
            "Content-Type": "application/json",
            "User-Agent": "tiingo-python-client {}".format(VERSION),
        }

        self._frequency_pattern = re.compile("^[0-9]+(min|hour)$", re.IGNORECASE)

    def __repr__(self):
        return '<TiingoClient(url="{}")>'.format(self._base_url)

    def _is_eod_frequency(self, frequency):
        return frequency.lower() in ["daily", "weekly", "monthly", "annually"]

    # TICKER PRICE ENDPOINTS
    # https://api.tiingo.com/docs/tiingo/daily
    def list_tickers(self, assetTypes=[]):
        """Return a list of dicts of metadata tickers for all supported tickers
         of the specified asset type, as well as metadata about each ticker.
         This includes supported date range, the exchange the ticker is traded
         on, and the currency the stock is traded on.
        Tickers for unrelated products are omitted.
        https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip
        """
        listing_file_url = (
            "https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip"
        )
        response = requests.get(listing_file_url)
        zipdata = get_zipfile_from_response(response)
        raw_csv = get_buffer_from_zipfile(zipdata, "supported_tickers.csv")
        reader = csv.DictReader(raw_csv)

        if not len(assetTypes):
            return [row for row in reader]

        assetTypesSet = set(assetTypes)
        return [row for row in reader if row.get("assetType") in assetTypesSet]

    def list_stock_tickers(self):
        return self.list_tickers(["Stock"])

    def list_etf_tickers(self):
        return self.list_tickers(["ETF"])

    def list_fund_tickers(self):
        return self.list_tickers(["Mutual Fund"])

    def get_ticker_metadata(self, ticker, fmt="json"):
        """Return metadata for 1 ticker
        Use TiingoClient.list_tickers() to get available options

         Args:
             ticker (str) : Unique identifier for stock
        """
        url = "tiingo/daily/{}".format(ticker)
        response = self._request("GET", url)
        data = response.json()
        if fmt == "json":
            return data
        elif fmt == "object":
            return dict_to_object(data, "Ticker")

    def _invalid_frequency(self, frequency):
        """
        Check to see that frequency was specified correctly
        :param frequency (string): frequency string
        :return (boolean):
        """
        is_valid = self._is_eod_frequency(frequency) or re.match(
            self._frequency_pattern, frequency
        )
        return not is_valid

    def _get_url(self, ticker, frequency):
        """
        Return url based on frequency.  Daily, weekly, or yearly use Tiingo
        EOD api; anything less than daily uses the iex intraday api.
        :param ticker (string): ticker to be embedded in the url
        :param frequency (string): valid frequency per Tiingo api
        :return (string): url
        """
        if self._invalid_frequency(frequency):
            etext = (
                "Error: {} is an invalid frequency.  Check Tiingo API documentation "
                "for valid EOD or intraday frequency format."
            )
            raise InvalidFrequencyError(etext.format(frequency))
        else:
            if self._is_eod_frequency(frequency):
                return "tiingo/daily/{}/prices".format(ticker)
            else:
                return "iex/{}/prices".format(ticker)

    def _request_pandas(self, ticker, metric_name, params):
        """
        Return data for ticker as a pandas.DataFrame if metric_name is not
        specified or as a pandas.Series if metric_name is specified.

        :param ticker (string): ticker to be requested
        :param params (dict): a dictionary containing valid resampleFreq
            and format strings per the Tiingo api
        :param metric_name (string): Optional parameter specifying metric to be returned for each
            ticker.  In the event of a single ticker, this is optional and if not specified
            all of the available data will be returned.  In the event of a list of tickers,
            this parameter is required.
        """
        url = self._get_url(ticker, params["resampleFreq"])
        response = self._request("GET", url, params=params)
        if params["format"] == "csv":
            if sys.version_info < (3, 0):  # python 2
                from StringIO import StringIO
            else:  # python 3
                from io import StringIO

            df = pd.read_csv(StringIO(response.content.decode("utf-8")))
        else:
            df = pd.DataFrame(response.json())

        df.set_index("date", inplace=True)

        if metric_name is not None:
            prices = df[metric_name]
        else:
            prices = df

        prices.index = pd.to_datetime(prices.index)

        # Localize to UTC to ensure equivalence between data returned in json format and
        # csv format. Tiingo daily data requested in csv format does not include a timezone.
        if prices.index.tz is None:
            prices.index = prices.index.tz_localize("UTC")

        return prices

    def get_ticker_price(
        self,
        ticker,
        startDate=None,
        endDate=None,
        columns=None,
        fmt="json",
        frequency="daily",
    ):
        """By default, return latest EOD Composite Price for a stock ticker.
        On average, each feed contains 3 data sources.

         Supported tickers + Available Day Ranges are here:
         https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip

         Args:
             ticker (string): Unique identifier for stock ticker
             startDate (string): Start of ticker range in YYYY-MM-DD format
             endDate (string): End of ticker range in YYYY-MM-DD format
             columns (string): Optional comma separated parameter specifying which columns to retrieve.
                By default, 'date', 'open', 'close', 'high' and 'low' are retrieved. 'volume' is an extra option.
             fmt (string): 'csv' or 'json'
             frequency (string): Resample frequency
        """
        url = self._get_url(ticker, frequency)
        params = {
            "format": fmt if fmt != "object" else "json",  # conversion local
            "resampleFreq": frequency,
        }

        if startDate:
            params["startDate"] = startDate
        if endDate:
            params["endDate"] = endDate
        if columns:
            params["columns"] = columns

        # TODO: evaluate whether to stream CSV to cache on disk, or
        # load as array in memory, or just pass plain text
        response = self._request("GET", url, params=params)
        if fmt == "json":
            return response.json()
        elif fmt == "object":
            data = response.json()
            return [dict_to_object(item, "TickerPrice") for item in data]
        else:
            return response.content.decode("utf-8")

    def get_dataframe(
        self,
        tickers,
        startDate=None,
        endDate=None,
        metric_name=None,
        columns=None,
        frequency="daily",
        fmt="json",
    ):
        """Return a pandas.DataFrame of historical prices for one or more ticker symbols.

        By default, return latest EOD Composite Price for a list of stock tickers.
        On average, each feed contains 3 data sources.

        Supported tickers + Available Day Ranges are here:
        https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip
        or from the TiingoClient.list_tickers() method.

        Args:
            tickers (string/list): One or more unique identifiers for a stock ticker.
            startDate (string): Start of ticker range in YYYY-MM-DD format.
            endDate (string): End of ticker range in YYYY-MM-DD format.
            columns (string): Optional comma separated parameter specifying which columns to retrieve.
                By default, 'date', 'open', 'close', 'high' and 'low' are retrieved. 'volume' is an extra option.
            metric_name (string): Optional parameter specifying metric to be returned for each
                ticker.  In the event of a single ticker, this is optional and if not specified
                all of the available data will be returned.  In the event of a list of tickers,
                this parameter is required.
            frequency (string): Resample frequency (defaults to daily).
            fmt (string): 'csv' or 'json'
        """

        valid_columns = {
            "open",
            "high",
            "low",
            "close",
            "volume",
            "adjOpen",
            "adjHigh",
            "adjLow",
            "adjClose",
            "adjVolume",
            "divCash",
            "splitFactor",
        }

        if metric_name is not None and metric_name not in valid_columns:
            raise APIColumnNameError("Valid data items are: " + str(valid_columns))

        if metric_name is None and isinstance(tickers, list):
            raise MissingRequiredArgumentError(
                """When tickers is provided as a list, metric_name is a required argument.
            Please provide a metric_name, or call this method with one ticker at a time."""
            )

        params = {"format": fmt, "resampleFreq": frequency}
        if startDate:
            params["startDate"] = startDate
        if endDate:
            params["endDate"] = endDate
        if columns:
            params["columns"] = columns

        if pandas_is_installed:
            if type(tickers) is str:
                prices = self._request_pandas(
                    ticker=tickers, params=params, metric_name=metric_name
                )
            else:
                prices = pd.DataFrame()
                for stock in tickers:
                    ticker_series = self._request_pandas(
                        ticker=stock, params=params, metric_name=metric_name
                    )
                    ticker_series = ticker_series.rename(stock)
                    prices = pd.concat([prices, ticker_series], axis=1, sort=True)

            return prices

        else:
            error_message = (
                "Pandas is not installed, but .get_ticker_price() was "
                "called with fmt=pandas.  In order to install tiingo with "
                "pandas, reinstall with pandas as an optional dependency. \n"
                "Install tiingo with pandas dependency: 'pip install tiingo[pandas]'\n"
                "Alternatively, just install pandas: pip install pandas."
            )
            raise InstallPandasException(error_message)

    # NEWS FEEDS
    # tiingo/news
    def get_news(
        self,
        tickers=[],
        tags=[],
        sources=[],
        startDate=None,
        endDate=None,
        limit=100,
        offset=0,
        sortBy="publishedDate",
        onlyWithTickers=False,
        fmt="json",
    ):
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
            sortBy (string): "publishedDate" OR "crawlDate", descending
            onlyWithTickers (bool): If true, only links with tagged tickers will return.
        """
        url = "tiingo/news"
        params = {
            "limit": limit,
            "offset": offset,
            "sortBy": sortBy,
            "tickers": tickers,
            "source": (",").join(sources) if sources else None,
            "tags": tags,
            "startDate": startDate,
            "endDate": endDate,
            "onlyWithTickers": onlyWithTickers,
        }
        response = self._request("GET", url, params=params)
        data = response.json()
        if fmt == "json":
            return data
        elif fmt == "object":
            return [dict_to_object(item, "NewsArticle") for item in data]

    def get_bulk_news(self, file_id=None, fmt="json"):
        """Only available to institutional clients.
        If ID is NOT provided, return array of available file_ids.
        If ID is provided, provides URL which you can use to download your
        file, as well as some metadata about that file.
        """
        if file_id:
            url = "tiingo/news/bulk_download/{}".format(file_id)
        else:
            url = "tiingo/news/bulk_download"

        response = self._request("GET", url)
        data = response.json()
        if fmt == "json":
            return data
        elif fmt == "object":
            return dict_to_object(data, "BulkNews")

    # Crypto
    # tiingo/crypto
    def get_crypto_top_of_book(
        self,
        tickers=[],
        exchanges=[],
        includeRawExchangeData=False,
        convertCurrency=None,
    ):
        url = "tiingo/crypto/top"
        params = {"tickers": ",".join(tickers)}

        if len(exchanges):
            params["exchanges"] = ",".join(exchanges)
        if includeRawExchangeData is True:
            params["includeRawExchangeData"] = True
        if convertCurrency:
            params["convertCurrency"] = convertCurrency

        response = self._request("GET", url, params=params)
        return response.json()

    def get_crypto_price_history(
        self,
        tickers=[],
        baseCurrency=None,
        startDate=None,
        endDate=None,
        exchanges=[],
        consolidateBaseCurrency=False,
        includeRawExchangeData=False,
        resampleFreq=None,
        convertCurrency=None,
    ):
        url = "tiingo/crypto/prices"
        params = {"tickers": ",".join(tickers)}

        if startDate:
            params["startDate"] = startDate
        if endDate:
            params["endDate"] = endDate
        if len(exchanges):
            params["exchanges"] = ",".join(exchanges)
        if consolidateBaseCurrency is True:
            params["consolidateBaseCurrency"] = ",".join(consolidateBaseCurrency)
        if includeRawExchangeData is True:
            params["includeRawExchangeData"] = includeRawExchangeData
        if resampleFreq:
            params["resampleFreq"] = resampleFreq
        if convertCurrency:
            params["convertCurrency"] = convertCurrency

        response = self._request("GET", url, params=params)
        return response.json()

    def get_crypto_metadata(self, tickers=[], fmt="json"):
        url = "tiingo/crypto"

        params = {
            "tickers": ",".join(tickers),
            "format": fmt,
        }

        response = self._request("GET", url, params=params)
        if fmt == "csv":
            return response.content.decode("utf-8")
        else:
            return response.json()

    # FUNDAMENTAL DEFINITIONS
    # tiingo/fundamentals/definitions
    def get_fundamentals_definitions(self, tickers=[], fmt="json"):
        """Return definitions for fundamentals for specified tickers
        https://api.tiingo.com/documentation/fundamentals

        Args:
            tickers [string] : optional, either list or string
            fmt (string): 'csv' or 'json'
        """
        url = "tiingo/fundamentals/definitions"
        params = {"tickers": tickers, "format": fmt}
        response = self._request("GET", url, params=params)
        if fmt == "json":
            return response.json()
        elif fmt == "csv":
            return response.content.decode("utf-8")

    # FUNDAMENTAL DAILY
    # tiingo/fundamentals/<ticker>/daily
    def get_fundamentals_daily(self, ticker, fmt="json", startDate=None, endDate=None):
        """Returns metrics which rely on daily price-updates
        https://api.tiingo.com/documentation/fundamentals

        # Dates are in YYYY-MM-DD Format.

        Args:
            tickers [string] : List of unique Stock Tickers to search
            startDate, endDate [date]: Boundaries of search window
            fmt (string): 'csv' or 'json'
        """
        url = "tiingo/fundamentals/{}/daily".format(ticker)
        params = {"startDate": startDate, "endDate": endDate, "format": fmt}
        response = self._request("GET", url, params=params)
        if fmt == "json":
            return response.json()
        elif fmt == "csv":
            return response.content.decode("utf-8")

    # FUNDAMENTAL STATEMENTS
    # tiingo/fundamentals/<ticker>/statements
    def get_fundamentals_statements(
        self, ticker, asReported=False, fmt="json", startDate=None, endDate=None
    ):
        """Returns data that is extracted from quarterly and annual statements.
            https://api.tiingo.com/documentation/fundamentals

            # Dates are in YYYY-MM-DD Format.

            Args:
                tickers [string] : List of unique Stock Tickers to search
                startDate, endDate [date]: Boundaries of search window
                asReported [bool]: get most-recent data (False) or data \
                                   as it was reported on the release-date
                                   (True)
                fmt (string): 'csv' or 'json'
        """
        if asReported:
            asReported = "true"
        else:
            asReported = "false"

        url = "tiingo/fundamentals/{}/statements".format(ticker)
        params = {
            "startDate": startDate,
            "endDate": endDate,
            "asReported": asReported,
            "format": fmt,
        }
        response = self._request("GET", url, params=params)
        if fmt == "json":
            return response.json()
        elif fmt == "csv":
            return response.content.decode("utf-8")
