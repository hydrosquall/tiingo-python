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

.. image:: https://img.shields.io/codecov/c/github/hydrosquall/tiingo-python.svg?maxAge=600
     :target: https://codecov.io/gh/hydrosquall/tiingo-python
     :alt: Coverage



Tiingo is a financial data platform that makes high quality financial tools available to all. They have a RESTful and Real-Time Data API. Presently, the API includes support for the following endpoints:

* Stock Market Ticker Closing Prices + Metadata. Data includes full distribution details and is validated using a proprietary EOD Price Engine.
* (Coming Soon): Curated news from top financial news sources + curated blogs. Stories are tagged by Tiingo's algorithms.


Usage
--------

First, install the library from PyPi:

.. code-block:: shell

   pip install tiingo

Next, initialize your client object. It is recommended to use an environment
variable to initialize your client object for convenience.

.. code-block:: python

  from tiingo import TiingoClient
  # Set TIINGO_API_KEY in your environment variables in your .bash_profile, OR
  # pass a dictionary with 'api_key' as a key into the TiingoClient.

  client = TiingoClient()

Alternately, you may use a dictionary to customize/authorize your client.

.. code-block:: python

  config = {}

  # To reuse the same HTTP Session across API calls (and have better performance), include a session key.
  config['session'] = True

  # If you don't have your API key as an environment variable,
  # pass it in via a configuration dictionary.
  config['api_key'] = "MY_SECRET_API_KEY"

  # Initialize
  client = TiingoClient(config)

Now you can use ``TiingoClient`` to make your API calls. (Other parameters are available for each endpoint beyond what has been written below, see the Tiingo website for full details).

.. code-block:: python
  
  # Get Ticker
  # See official docs for list of all supported tickers + date ranges
  ticker_metadata = client.get_ticker_metadata("GOOGL")

  # Get latest prices, based on 3+ sources, as CSV or JSON, sampled weekly
  ticker_price = client.get_ticker_price("GOOGL", frequency="weekly")

  # Get news articles about given tickers or search terms from given domains
  # Coming soon!


Further Docs
--------

* Official Tiingo Documentation: https://api.tiingo.com
* Tiingo-Python Documentation (Under Construction): https://tiingo-python.readthedocs.io.

Features
--------

* Easy programmatic access to Tiingo API
# Ability to reuse session across API calls for better performance
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
