#!/usr/bin/env python
"""Tests for `tiingo` package."""

from unittest import TestCase

import vcr

from tiingo import TiingoClient


# CRYPTO ENDPOINTS
class TestCryptoEndpoints(TestCase):

    def setUp(self):
        self._client = TiingoClient()

    @vcr.use_cassette('tests/fixtures/crypto_metadata.yaml')
    def test_crypto_metadata(self):
        metadata = self._client.get_crypto_metadata(tickers=['btcusd', 'fldcbtc'])

        assert len(metadata) == 2 # 1 item per ticker
        assert metadata[0]['ticker'] == 'btcusd'
        assert metadata[1]['ticker'] == 'fldcbtc'

    @vcr.use_cassette('tests/fixtures/crypto_top_of_book.yaml')
    def test_crypto_top_of_book(self):
        top_of_book = self._client.get_crypto_top_of_book(tickers=['btcusd', 'fldcbtc'], includeRawExchangeData=True)
        assert len(top_of_book) == 2 # 1 each for btcusd and fldcbtc
        first_ticker_data = top_of_book[0]
        assert 'topOfBookData' in first_ticker_data
        assert 'exchangeData' in first_ticker_data

    @vcr.use_cassette('tests/fixtures/crypto_price_history.yaml')
    def test_crypto_price_history(self):
        price_history = self._client.get_crypto_price_history(tickers=['btcusd', 'fldcbtc'],
                                                              startDate='2019-05-01', endDate='2019-05-02',
                                                              includeRawExchangeData=True, resampleFreq='1day')
        assert len(price_history) == 2 # 1 item per ticker
        assert len(price_history[0]['priceData']) == 2 # 1 set of data per day
        assert 'exchangeData' in price_history[0] # includedRawExchangeData
