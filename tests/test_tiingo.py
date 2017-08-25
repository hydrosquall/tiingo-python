#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tiingo` package."""

import pytest

from tiingo import TiingoClient


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    t = TiingoClient()
    return t.get_ticker_price("GOOGL")
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    assert len(response) > 0
