# -*- coding: utf-8 -*-
# @Author: Cameron Yick


from unittest import TestCase

import vcr

from tiingo.restclient import (RestClient, RestClientError)

# Tests of basic REST API functionality
BASE_URL = "http://www.google.com"


# Test valid url
class TestRestClient(TestCase):

    def setUp(self):
        client = RestClient()
        client._base_url = BASE_URL
        client._headers = {}
        self._client = client

    # Test Requests
    def test_client_representation(self):
        self.assertEqual(repr(self._client),
                         "<RestClient(url=\"{}\")>".format(BASE_URL))

    # Test valid page
    def test_valid_url(self):
        with vcr.use_cassette('tests/fixtures/valid_url.yaml'):
            response = self._client._request('GET', "")
        self.assertEqual(response.status_code, 200)

    # Test 404 error
    def test_invalid_url(self):
        with self.assertRaisesRegexp(RestClientError, "404"),\
                vcr.use_cassette('tests/fixtures/invalid_url.yaml'):
            # Should return 404 error
            self._client._request('GET', "bing_is_great")

    # Todo: try using an invalid HTTP method (i.e. SNAG) and catch the error


# Check if everything still works when a session is reused
# TODO: Figure how how to refactor so that we can run these same 3 tests,
# except with 2 different types of client.
class TestRestClientWithSession(TestCase):
    def setUp(self):
        config = {'session': True}
        client = RestClient(config)
        client._base_url = BASE_URL
        client._headers = {}
        self._client = client

    # Test Requests
    def test_client_representation(self):
        self.assertEqual(repr(self._client),
                         "<RestClient(url=\"{}\")>".format(BASE_URL))

    # Test valid page
    def test_valid_url(self):
        with vcr.use_cassette('tests/fixtures/valid_url.yaml'):
            response = self._client._request('GET', "")
        self.assertEqual(response.status_code, 200)

    # Test 404 error
    def test_invalid_url(self):
        with self.assertRaisesRegexp(RestClientError, "404"),\
                vcr.use_cassette('tests/fixtures/invalid_url.yaml'):
            # Should return 404 error
            self._client._request('GET', "bing_is_great")
