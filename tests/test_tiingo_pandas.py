#!/usr/bin/env python
"""Unit tests for pandas functionality in tiingo"""

import vcr
from unittest import TestCase
from tiingo import TiingoClient
from tiingo.api import APIColumnNameError, InstallPandasException
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

    @vcr.use_cassette('tests/fixtures/ticker_price_pandas_weekly_multiple_tickers.yaml')
    def test_return_pandas_format_multiple(self):
        """Test that valid pandas format is returned when specified"""
        tickers = ["GOOGL", "AAPL"]
        prices = self._client.get_dataframe(tickers, startDate='2018-01-05',
                                            endDate='2018-01-19', metric_name='adjClose', frequency='weekly')
        self.assertTrue(isinstance(prices, pd.DataFrame))
        assert prices['GOOGL'].loc['2018-01-05'] == 1110.29
        self.assertAlmostEqual(prices['AAPL'].loc['2018-01-19'], 178.54, 2)

    @vcr.use_cassette('tests/fixtures/ticker_price_pandas_daily.yaml')
    def test_return_pandas_daily(self):
        """Test that valid pandas format is returned when specified"""
        prices = self._client.get_dataframe("GOOGL", startDate='2018-01-05',
                                            endDate='2018-01-19', frequency='daily')
        self.assertTrue(isinstance(prices, pd.DataFrame))
        assert prices['adjClose'].loc['2018-01-05'] == 1110.29

    def test_column_error(self):
        with self.assertRaises(APIColumnNameError):
            self._client.get_dataframe(['GOOGL', 'AAPL'], startDate='2018-01-05',
                                                endDate='2018-01-19', metric_name='xopen', frequency='weekly')
    @vcr.use_cassette('tests/fixtures/ticker_price_pandas_single.yaml')
    def test_pandas_edge_case(self):
        """Test single price/date being returned as a frame"""
        prices = self._client.get_dataframe("GOOGL")
        assert len(prices) == 1
        assert len(prices.index) == 1


class TestTiingoWithoutPython(TestCase):

    def setUp(self):
        if pandas_is_installed:
            self.skipTest("test_tiingo_without_pandas: Pandas not installed.")
        else:
            self._client = TiingoClient()

    @vcr.use_cassette('tests/fixtures/ticker_price_pandas_single.yaml')
    def test_get_dataframe_without_pandas(self):
        with self.assertRaises(InstallPandasException):
            self._client.get_dataframe("GOOGL")
