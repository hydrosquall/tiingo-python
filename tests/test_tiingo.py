#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `tiingo` package."""

import pytest
from tiingo import TiingoClient

# TODO
# Add tests for
# Invalid API key
# Invalid ticker, etc
# Use unittest asserts rather than regular asserts
# Wrap server errors with client side descriptive errors
# Coerce startDate/endDate to string if they are passed in as datetime
# Use VCR.py to enable offline testing


# Refactor fixtures into separate file
@pytest.fixture
def ticker_price_response():
    """Test /tiingo/<ticker>/prices endpoint"""
    t = TiingoClient()
    return t.get_ticker_price("GOOGL")


@pytest.fixture
def ticker_metadata_response():
    """Test /tiingo/<ticker> endpoint"""
    t = TiingoClient()
    return t.get_ticker_metadata("GOOGL")


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


# PRICES ENDPOINTS
class TestTickerPrices(object):
    def test_ticker_price(self, ticker_price_response):
        """Test the EOD Prices Endpoint"""
        assert len(ticker_price_response) == 1
        assert ticker_price_response[0].get('adjClose')

    def test_ticker_metadata(self, ticker_metadata_response):
        """Refactor this with python data schemavalidation"""
        assert ticker_metadata_response.get('ticker') == "GOOGL"
        assert ticker_metadata_response.get("name")


# FUND ENDPOINTS
@pytest.mark.skip(reason="My API key doesn't have access to mutual funds API")
class TestMutualFunds(object):

    def test_fund_metadata(self, fund_metadata_response):
        """Refactor this with python data schemavalidation"""
        assert fund_metadata_response.get('ticker') == "vfinx"
        assert fund_metadata_response.get("shareClass", startDate="2012-1-1",
                                          endDate="2016-1-1")

    def test_fund_metrics(self, fund_metrics_response):
        """Test Fund Level Metrics"""
        assert len(fund_metrics_response) > 0
        assert fund_metrics_response[0].get('managementFee')
