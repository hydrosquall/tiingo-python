#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tiingo` package."""

import pytest

from tiingo import TiingoClient


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


def test_ticker_price(ticker_price_response):
    """Sample pytest test function with the pytest fixture as an argument."""
    assert len(ticker_price_response) == 1
    assert ticker_price_response.get('adjClose')


def test_ticker_metadata(ticker_metadata_response):
    """Refactor this with python data schemavalidation"""
    assert ticker_metadata_response.get('ticker') == "GOOGL"
    assert ticker_metadata_response.get("name")
