=============
Tiingo Python
=============


.. image:: https://img.shields.io/pypi/v/tiingo.svg
        :target: https://pypi.python.org/pypi/tiingo

.. image:: https://img.shields.io/travis/hydrosquall/tiingo-python.svg
        :target: https://travis-ci.org/hydrosquall/tiingo-python

.. image:: https://readthedocs.org/projects/tiingo-python/badge/?version=latest
        :target: https://tiingo-python.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/hydrosquall/tiingo-python/shield.svg
     :target: https://pyup.io/repos/github/hydrosquall/tiingo-python/
     :alt: Updates

.. image:: https://codecov.io/gh/hydrosquall/tiingo-python/branch/master/graph/badge.svg
     :target: https://codecov.io/gh/hydrosquall/tiingo-python
     :alt: Coverage



Tiingo is a financial data platform that makes high quality financial tools available to all. They have a RESTful and Real-Time Data API. Presently, the API includes support for the following endpoints:

* Stock Market Ticker Closing Prices + Metadata. Data includes full distribution details and is validated using a proprietary EOD Price Engine.
* Mutual Funds Metadata + Metrics updated daily. Supports over 26,500 Mutual Funds and ETFs.
* (Coming Soon): Curated news from top financial news sources + curated blogs. Stories are tagged by Tiingo's algorithms.


Usage
--------

First, install the library from PyPi:

.. code-block:: shell

   pip install tiingo

Now you can use the TiingoClient to make your API calls. (Other parameters are available for each endpoint beyond what has been written below, see docs for full details.)

.. code-block:: python

   from tiingo import TiingoClient
   # Set TIINGO_API_KEY in your environment variables in your .bash_profile, OR
   # pass a dictionary with 'api_key' as a key into the TiingoClient.

   # With environment variable
   client = TiingoClient()
   # With hardcoded dictionary key
   client = TiingoClient({'api_key': "MY_SECRET_API_KEY"})

   # Get Ticker
   # See official docs for list of all supported tickers + date ranges
   ticker_metadata = client.get_ticker_metadata("GOOGL")

   # Get latest prices, based on 3+ sources, as CSV or JSON, sampled weekly
   ticker_price = client.get_ticker_price("GOOGL", frequency="weekly")

   # WARNING: These will only work if your account has access to the 
   # Mutual Funds portion of the API.
   # Get mutual fund metadata
   fund_metadata = client.get_fund_metadata("VFINX")
   # Get mutual fund Expenses and Shareholder Fee Data for June 2017
   fund_metrics = client.get_fund_metrics("VFINX", "2017-06-01", "2017-06-30")

   # Get news articles about given tickers or search terms from given domains
   # Coming soon!

Further Docs
--------

* Official Tiingo Documentation: https://api.tiingo.com
* Tiingo-Python Documentation (Under Construction): https://tiingo-python.readthedocs.io.

Features
--------

* Easy programmatic access to Tiingo API
* Coming soon: 
    * Client-side validation of tickers, to save your API calls!
    * Data validation of returned responses 
    * Case insensitivity


Credits
---------

* Many thanks to Rishi Singh for creating Tiingo.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
