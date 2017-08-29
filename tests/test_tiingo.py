#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `tiingo` package."""

import csv
import pytest
from unittest import TestCase
from tiingo import TiingoClient


# TODO
# Add tests for
# Invalid API key
# Invalid ticker, etc
# Use unittest asserts rather than regular asserts
# Wrap server errors with client side descriptive errors
# Coerce startDate/endDate to string if they are passed in as datetime
# Use VCR.py to enable offline testing
# Expand test coverage


@pytest.fixture
def fund_metadata_response():
    """Test /tiingo/<ticker> endpoint"""
    t = TiingoClient()
    return t.get_fund_metadata("vfinx")


@pytest.fixture
def fund_metrics_response():
    """Test /tiingo/<ticker> endpoint"""
    t = TiingoClient()
    return t.get_fund_metrics("VFINX")


def test_client_repr():
    """Test representation of client when logged to console"""
    client = TiingoClient()
    base_url = "https://api.tiingo.com"
    assert repr(client) == "<TiingoClient(url=\"{}\")>".format(base_url)


# PRICES ENDPOINTS
class TestTickerPrices(TestCase):

    def setUp(self):
        self._client = TiingoClient()
        # Stub all endpoints that get reused
        self._ticker_price_response = self._client.get_ticker_price("GOOGL")
        self._ticker_metadata_response = \
            self._client.get_ticker_metadata("GOOGL")

    def test_ticker_price(self):
        """Test the EOD Prices Endpoint"""
        assert len(self._ticker_price_response) == 1
        assert self._ticker_price_response[0].get('adjClose')

    def test_ticker_price_with_date(self):
        """Test the EOD Prices Endpoint with data param"""
        prices = self._client.get_ticker_price("GOOGL",
                                               startDate="2015-01-01",
                                               endDate="2015-01-05")
        self.assertGreater(len(prices), 1)

    def test_ticker_price_with_csv(self):
        """Confirm that CSV endpoint works"""
        prices_csv = self._client.get_ticker_price("GOOGL",
                                                   startDate="2015-01-01",
                                                   endDate="2015-01-05",
                                                   fmt='csv')
        reader = csv.reader(prices_csv.splitlines(), delimiter=",")
        rows = list(reader)
        assert len(rows) > 2  # more than 1 day of data

    def test_ticker_metadata(self):
        """Refactor this with python data schemavalidation"""
        assert self._ticker_metadata_response.get('ticker') == "GOOGL"
        assert self._ticker_metadata_response.get("name")

    def test_list_tickers(self):
        """Update this test when the method is added."""
        with self.assertRaises(NotImplementedError):
            response = self._client.list_tickers()
            assert not response


# FUND ENDPOINTS
# tiingo/funds
# Try to get a working API key from Tiingo development for testing purposes
@pytest.mark.skip(reason="My API key doesn't have access to mutual funds API")
class TestMutualFunds(TestCase):

    def test_fund_metadata(self, fund_metadata_response):
        """Refactor this with python data schemavalidation"""
        assert fund_metadata_response.get('ticker') == "vfinx"
        assert fund_metadata_response.get("shareClass", startDate="2012-1-1",
                                          endDate="2016-1-1")

    def test_fund_metrics(self, fund_metrics_response):
        """Test Fund Level Metrics"""
        assert len(fund_metrics_response) > 0
        assert fund_metrics_response[0].get('managementFee')


# News Feed
# tiingo/news
class TestNews(TestCase):

    def setUp(self):
        self._client = TiingoClient()

    def test_get_news_articles(self):
        """Rewrite when method is implemented
        """
        with self.assertRaises(NotImplementedError) as context:
            self.get_news()
            print(context)
