#!/usr/bin/env python
"""Unit tests for pandas functionality in tiingo"""

import vcr
from unittest import TestCase
from tiingo import TiingoClient
from tiingo.exceptions import APIColumnNameError, InstallPandasException, MissingRequiredArgumentError
try:
    import pandas as pd
    pandas_is_installed = True
except ImportError:
    pandas_is_installed = False


class TestTiingoWithPython(TestCase):

    def setUp(self):
        if pandas_is_installed:
            self._client = TiingoClient()
        else:
            self.skipTest("test_tiingo_pandas: Pandas not installed.")

    @vcr.use_cassette('tests/fixtures/ticker_price_pandas_weekly.yaml')
    def test_return_pandas_format(self):
        """Test that valid pandas format is returned when specified"""
        prices = self._client.get_dataframe("GOOGL", startDate='2018-01-05',
                                            endDate='2018-01-19', frequency='weekly')
        self.assertTrue(isinstance(prices, pd.DataFrame))
        assert len(prices.index) == 3

    @vcr.use_cassette('tests/fixtures/ticker_price_pandas_weekly_multiple_tickers.yaml')
    def test_return_pandas_format_multiple(self):
        """Test that valid pandas format is returned when specified"""
        tickers = ["GOOGL", "AAPL"]
        prices = self._client.get_dataframe(tickers, startDate='2018-01-05',
                                            endDate='2018-01-19', metric_name='adjClose', frequency='weekly')
        self.assertTrue(isinstance(prices, pd.DataFrame))
        assert len(prices.columns) == 2
        assert len(prices.index) == 3

    @vcr.use_cassette('tests/fixtures/ticker_price_pandas_daily.yaml')
    def test_return_pandas_daily(self):
        """Test that valid pandas format is returned when specified"""
        prices = self._client.get_dataframe("GOOGL", startDate='2018-01-05',
                                            endDate='2018-01-19', frequency='daily')
        self.assertTrue(isinstance(prices, pd.DataFrame))
        assert len(prices.columns) == 12

    @vcr.use_cassette('tests/fixtures/ticker_price_pandas_daily_metric_name.yaml')
    def test_return_pandas_daily(self):
        """Test that one column is returned when a metric name is specified"""

        prices = self._client.get_dataframe("GOOGL", startDate='2018-01-05', metric_name='adjClose',
                                            endDate='2018-01-19', frequency='daily')
        self.assertTrue(isinstance(prices, pd.Series))
        assert len(prices.index) == 10

    @vcr.use_cassette('tests/fixtures/intraday_price.yaml')
    def test_intraday_ticker_price(self):
        """Test the EOD Prices Endpoint with data param"""
        prices = self._client.get_dataframe("GOOGL",
                                            startDate="2018-01-02",
                                            endDate="2018-01-02",
                                            frequency="30Min")
        self.assertGreater(len(prices), 1)

    def test_metric_name_column_error(self):
        with self.assertRaises(APIColumnNameError):
            self._client.get_dataframe(['GOOGL', 'AAPL'], startDate='2018-01-05',
                                                endDate='2018-01-19', metric_name='xopen', frequency='weekly')

    def test_metric_name_missing_when_multiple_tickers(self):
        with self.assertRaises(MissingRequiredArgumentError):
            self._client.get_dataframe(['GOOGL', 'AAPL'], frequency='weekly')

    @vcr.use_cassette('tests/fixtures/ticker_price_pandas_single.yaml')
    def test_pandas_edge_case(self):
        """Test single price/date being returned as a frame"""
        prices = self._client.get_dataframe("GOOGL")
        assert len(prices) == 1
        assert len(prices.index) == 1


class TestTiingoWithoutPython(TestCase):

    def setUp(self):
        if pandas_is_installed:
            self.skipTest("test_tiingo_without_pandas: Pandas is installed.")
        else:
            self._client = TiingoClient()

    @vcr.use_cassette('tests/fixtures/ticker_price_pandas_single.yaml')
    def test_get_dataframe_without_pandas(self):
        with self.assertRaises(InstallPandasException):
            self._client.get_dataframe("GOOGL")
