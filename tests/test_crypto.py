#!/usr/bin/env python
"""Tests for `tiingo` package."""

from unittest import TestCase

from tiingo import TiingoClient


# CRYPTO ENDPOINTS
class TestCryptoEndpoints(TestCase):

    def setUp(self):
        self._client = TiingoClient()

    def test_crypto_metadata(self):
        metadata = self._client.get_crypto_meta_data(ticker=['btcusd', 'fldcbtc'])

        assert len(metadata) == 2
        assert metadata[0].ticker == 'btcusd'
        assert metadata[1].ticker == 'fldcbtc'

    def test_crypto_top_of_book(self):
        top_of_book = self._client.get_crypto_top_of_book(tickers=['btcusd', 'fldcbtc'],
                                                          endDate='2018-01-02', includeRawExchangeData=True)
        assert 'topOfBookData' in top_of_book
        assert len(top_of_book['topOfBookData']) == 2
        assert 'exchangeData' in top_of_book

    def test_crypto_price_history(self):
        price_history = self._client.get_crypto_price_history(tickers=['btcusd', 'fldcbtc'],
                                                              startDate='2019-05-01', endDate='2019-05-02',
                                                              includeRawExchangeData=True, resampleFreq='daily')
        assert len(price_history) == 2
        assert len(price_history[0]['priceData']) in [6, 7]
        assert 'exchangeData' in price_history[0]
