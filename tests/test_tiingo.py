#!/usr/bin/env python
"""Tests for `tiingo` package."""

import csv
from unittest import TestCase
import vcr

from tiingo import TiingoClient
from tiingo.exceptions import InvalidFrequencyError
from tiingo.restclient import RestClientError


# TODO
# Add tests for
# - Invalid API key
# - Invalid ticker
# Use unittest asserts rather than regular asserts if applicable
# Wrap server errors with client side descriptive errors
# Coerce startDate/endDate to string if they are passed in as datetime


def test_client_repr():
    """Test representation of client when logged to console"""
    client = TiingoClient()
    base_url = "https://api.tiingo.com"
    assert repr(client) == "<TiingoClient(url=\"{}\")>".format(base_url)


class TestClient(TestCase):

    def test_api_key_missing_error(self):
        config = {
            'api_key': ""
        }
        with self.assertRaises(RuntimeError):
            client = TiingoClient(config=config)
            assert client


# PRICES ENDPOINTS
class TestTickerPrices(TestCase):

    def setUp(self):
        self._client = TiingoClient()

    @vcr.use_cassette('tests/fixtures/ticker_metadata.yaml')
    def test_ticker_metadata(self):
        """Refactor this with python data schemavalidation"""
        metadata = self._client.get_ticker_metadata("GOOGL")

        assert metadata.get('ticker') == "GOOGL"
        assert metadata.get("name")

    @vcr.use_cassette('tests/fixtures/ticker_metadata.yaml')
    def test_ticker_metadata_as_object(self):
        metadata = self._client.get_ticker_metadata("GOOGL", fmt="object")
        assert metadata.ticker == "GOOGL"  # Access property via ATTRIBUTE
        assert metadata.name  # (contrast with key access above

    @vcr.use_cassette('tests/fixtures/ticker_price.yaml')
    def test_ticker_price(self):
        """Test that EOD Prices Endpoint works"""
        prices = self._client.get_ticker_price("GOOGL")
        assert len(prices) == 1
        assert prices[0].get('adjClose')

    @vcr.use_cassette('tests/fixtures/ticker_price_weekly.yaml')
    def test_ticker_price(self):
        """Test that weekly frequency works"""
        prices = self._client.get_ticker_price("GOOGL", startDate='2018-01-05',
                                               endDate='2018-01-19', frequency='weekly')
        assert len(prices) == 3
        assert prices[0].get('adjClose')

    @vcr.use_cassette('tests/fixtures/ticker_price.yaml')
    def test_ticker_price_as_object(self):
        """Test that EOD Prices Endpoint works"""
        prices = self._client.get_ticker_price("GOOGL", fmt="object")
        assert len(prices) == 1
        assert hasattr(prices[0], 'adjClose')

    @vcr.use_cassette('tests/fixtures/ticker_price_with_date.yaml')
    def test_ticker_price_with_date(self):
        """Test the EOD Prices Endpoint with data param"""
        prices = self._client.get_ticker_price("GOOGL",
                                               startDate="2015-01-01",
                                               endDate="2015-01-05")
        self.assertGreater(len(prices), 1)

    @vcr.use_cassette('tests/fixtures/ticker_price_with_date_csv.yaml')
    def test_ticker_price_with_csv(self):
        """Confirm that CSV endpoint works"""
        prices_csv = self._client.get_ticker_price("GOOGL",
                                                   startDate="2015-01-01",
                                                   endDate="2015-01-05",
                                                   fmt='csv')
        reader = csv.reader(prices_csv.splitlines(), delimiter=",")
        rows = list(reader)
        assert len(rows) > 2  # more than 1 day of data

    @vcr.use_cassette('tests/fixtures/ticker_price_with_volume_column.yaml')
    def test_ticker_price_with_volume_column(self):
        """Confirm that requesting a single column works"""
        prices = self._client.get_ticker_price("GOOGL",
                                               columns="volume",
                                               fmt='json')
        assert len(prices) == 1
        assert prices[0].get('date')
        assert not prices[0].get('high')
        assert not prices[0].get('low')
        assert not prices[0].get('open')
        assert not prices[0].get('close')
        assert prices[0].get('volume')

    @vcr.use_cassette('tests/fixtures/ticker_price_with_multiple_columns.yaml')
    def test_ticker_price_with_multiple_columns(self):
        """Confirm that requesting specific columns works"""
        requested_columns = "open,high,low,close,volume"
        prices = self._client.get_ticker_price("GOOGL",
                                               columns=requested_columns,
                                               fmt='json')
        assert len(prices) == 1
        assert len(prices[0]) == len(requested_columns.split(',')) + 1
        assert prices[0].get('date')
        assert prices[0].get('high')
        assert prices[0].get('low')
        assert prices[0].get('open')
        assert prices[0].get('close')
        assert prices[0].get('volume')

    @vcr.use_cassette('tests/fixtures/intraday_price.yaml')
    def test_intraday_ticker_price(self):
        """Test the EOD Prices Endpoint with data param"""
        prices = self._client.get_ticker_price("GOOGL",
                                               startDate="2018-01-02",
                                               endDate="2018-01-02",
                                               frequency="30Min")
        self.assertGreater(len(prices), 1)

    @vcr.use_cassette('tests/fixtures/list_all_tickers.yaml')
    def test_list_all_tickers(self):
        tickers = self._client.list_tickers()
        assert len(tickers) > 1
        assert any(ticker['assetType'] == 'Stock' for ticker in tickers)
        print(tickers)
        assert any(ticker['assetType'] == 'Mutual Fund' for ticker in tickers)
        assert any(ticker['assetType'] == 'ETF' for ticker in tickers)

    @vcr.use_cassette('tests/fixtures/list_all_tickers.yaml')
    def test_list_multi_tickers(self):
        tickers = self._client.list_tickers(['Stock', 'ETF'])
        assert len(tickers) > 1
        assert any(ticker['assetType'] == 'Stock' for ticker in tickers)
        assert any(ticker['assetType'] == 'ETF' for ticker in tickers)
        assert all(ticker['assetType'] != 'Mutual Fund' for ticker in tickers)

    @vcr.use_cassette('tests/fixtures/list_all_tickers.yaml')
    def test_list_stock_tickers(self):
        tickers = self._client.list_stock_tickers()
        assert len(tickers) > 1
        assert all(ticker['assetType'] == 'Stock' for ticker in tickers)

    @vcr.use_cassette('tests/fixtures/list_fund_tickers.yaml')
    def test_list_fund_tickers(self):
        tickers = self._client.list_fund_tickers()
        assert len(tickers) > 1
        assert all(ticker['assetType'] == 'Mutual Fund' for ticker in tickers)

    @vcr.use_cassette('tests/fixtures/list_etf_tickers.yaml')
    def test_list_etf_tickers(self):
        tickers = self._client.list_etf_tickers()
        assert len(tickers) > 1
        assert all(ticker['assetType'] == 'ETF' for ticker in tickers)

    def test_invalid_frequency_error(self):
        with self.assertRaises(InvalidFrequencyError):
            prices = self._client.get_ticker_price("GOOGL",
                                                   startDate="2018-01-02",
                                                   endDate="2018-01-02",
                                                   frequency="1.5mins")


# tiingo/news
class TestNews(TestCase):

    def setUp(self):
        self._client = TiingoClient()
        self.article_keys = [  # Properties every article should have.
            'description',
            'title',
            'url',
            'publishedDate',
            'tags',
            'source',
            'tickers',
            'crawlDate',
            'id'
        ]
        # Search for articles about a topic
        self.num_articles = 1
        self.search_params = {
            "tickers": ["aapl", "googl"],
            "tags": ["Technology", "Bitcoin"],
            "startDate": "2016-01-01",
            "endDate": "2017-08-31",
            "sources": ['cnbc.com', 'altcointoday.com'],
            "limit": self.num_articles
        }

    @vcr.use_cassette('tests/fixtures/news.yaml')
    def test_get_news_articles(self):
        articles = self._client.get_news(**self.search_params)
        assert len(articles) == self.num_articles
        for article in articles:
            assert all(key in article for key in self.article_keys)

    @vcr.use_cassette('tests/fixtures/news_empty_sources.yaml')
    def test_get_news_empty_sources(self):
        search_params = self.search_params.copy()
        search_params['sources'] = []
        articles = self._client.get_news(**search_params)
        assert len(articles) == self.num_articles
        for article in articles:
            assert all(key in article for key in self.article_keys)

    @vcr.use_cassette('tests/fixtures/news_bulk.yaml')
    def test_get_news_bulk(self):
        """Fails because this API key lacks institutional license"""
        with self.assertRaises(RestClientError):
            value = self._client.get_bulk_news(file_id="1")
            assert value

    @vcr.use_cassette('tests/fixtures/news_bulk_file_ids.yaml')
    def test_get_news_bulk_ids(self):
        """Fails because this API key lacks institutional license"""
        with self.assertRaises(RestClientError):
            value = self._client.get_bulk_news()
            assert value

    # Tests "object" formatting option
    @vcr.use_cassette('tests/fixtures/news.yaml')
    def test_get_news_as_objects(self):
        articles = self._client.get_news(fmt="object", **self.search_params)
        assert len(articles) == self.num_articles
        for article in articles:  # check if attribute access works
            assert all(hasattr(article, key) for key in self.article_keys)

    @vcr.use_cassette('tests/fixtures/news_bulk_file_ids.yaml')
    def test_get_news_bulk_ids_as_objects(self):
        """Fails because this API key lacks institutional license"""
        with self.assertRaises(RestClientError):
            value = self._client.get_bulk_news(fmt="object")
            assert value

    @vcr.use_cassette('tests/fixtures/news_bulk.yaml')
    def test_news_bulk_as_objects(self):
        """Fails because this API key lacks institutional license"""
        with self.assertRaises(RestClientError):
            assert self._client.get_bulk_news(file_id="1", fmt="object")


# FUNDAMENTALS ENDPOINTS
class TestFundamentals(TestCase):

    def setUp(self):
        self._client = TiingoClient()

    @vcr.use_cassette('tests/fixtures/fundamentals_definitions.yaml')
    def test_definitions(self):
        definitions = self._client.get_fundamentals_definitions("GOOGL")
        assert len(definitions) > 1

    @vcr.use_cassette('tests/fixtures/fundamentals_definitions_csv.yaml')
    def test_definitions_csv(self):
        definitions = self._client.get_fundamentals_definitions("GOOGL",
                                                                fmt='csv')
        assert len(definitions) > 1

    @vcr.use_cassette('tests/fixtures/fundamentals_daily.yaml')
    def test_daily(self):
        daily = self._client.get_fundamentals_daily("GOOGL",
                                                    startDate='2020-1-1',
                                                    endDate='2020-4-1')
        assert len(daily) > 1

    @vcr.use_cassette('tests/fixtures/fundamentals_daily_csv.yaml')
    def test_daily_with_csv(self):
        daily = self._client.get_fundamentals_daily("GOOGL",
                                                    startDate='2020-1-1',
                                                    endDate='2020-4-1',
                                                    fmt='csv')
        assert len(daily) > 1

    @vcr.use_cassette('tests/fixtures/fundamentals_statements.yaml')
    def test_statements(self):
        statements = self._client.get_fundamentals_statements("GOOGL",
                                                              startDate='2020-1-1',
                                                              endDate='2020-4-1')
        assert len(statements) > 1

    @vcr.use_cassette('tests/fixtures/fundamentals_statements_with_as_reported.yaml')
    def test_statements(self):
        statements = self._client.get_fundamentals_statements("GOOGL",
                                                              startDate='2020-1-1',
                                                              endDate='2020-4-1',
                                                              asReported=True)
        assert len(statements) > 1

    @vcr.use_cassette('tests/fixtures/fundamentals_statements_csv.yaml')
    def test_statements_with_csv(self):
        statements = self._client.get_fundamentals_statements("GOOGL",
                                                              startDate='2020-1-1',
                                                              endDate='2020-4-1',
                                                              fmt='csv')
        assert len(statements) > 1
