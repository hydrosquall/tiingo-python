Tiingo Python
=============


.. image:: https://img.shields.io/pypi/v/tiingo.svg?maxAge=600
        :target: https://pypi.python.org/pypi/tiingo

.. image:: https://img.shields.io/codecov/c/github/hydrosquall/tiingo-python.svg?maxAge=600
     :target: https://codecov.io/gh/hydrosquall/tiingo-python
     :alt: Coverage

.. image:: https://readthedocs.org/projects/tiingo-python/badge/?version=latest&maxAge=600
        :target: https://tiingo-python.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/hydrosquall/tiingo-python/shield.svg?maxAge=600
     :target: https://pyup.io/repos/github/hydrosquall/tiingo-python/
     :alt: Updates

.. image:: https://mybinder.org/badge_logo.svg
     :target: https://mybinder.org/v2/gh/hydrosquall/tiingo-python/master?filepath=examples%2Fbasic-usage-with-pandas.ipynb
     :alt: Launch Binder



Tiingo is a financial data platform that makes high quality financial tools available to all. Tiingo has a REST and Real-Time Data API, which this library helps you to access. Presently, the API includes support for the following endpoints:

* Stock Market Ticker Closing Prices + Metadata. Data includes full distribution details and is validated using a proprietary EOD Price Engine.
* Curated news from top financial news sources + blogs. Stories are tagged with topic tags and relevant stock tickers by Tiingo's algorithms.


Usage
--------

If you'd like to try this library before installing, click below to open a folder of online runnable examples.

.. image:: https://mybinder.org/badge_logo.svg
     :target: https://mybinder.org/v2/gh/hydrosquall/tiingo-python/master?filepath=examples
     :alt: Launch Binder


First, install the library from PyPi:

.. code-block:: shell

   pip install tiingo

If you prefer to receive your results in ``pandas DataFrame`` or ``Series`` format, and you do not already have pandas installed, install it as an optional dependency:

.. code-block:: shell

   pip install tiingo[pandas]

Next, initialize your client. It is recommended to use an environment
variable to initialize your client for convenience.

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

Now you can use ``TiingoClient`` to make your API calls. (Other parameters are available for each endpoint beyond what is used in the below examples, inspect the docstring
for each function for details.).

.. code-block:: python

  # Get Ticker
  ticker_metadata = client.get_ticker_metadata("GOOGL")

  # Get latest prices, based on 3+ sources as JSON, sampled weekly
  ticker_price = client.get_ticker_price("GOOGL", frequency="weekly")

  # Get historical GOOGL prices from August 2017 as JSON, sampled daily
  historical_prices = client.get_ticker_price("GOOGL",
                                              fmt='json',
                                              startDate='2017-08-01',
                                              endDate='2017-08-31',
                                              frequency='daily')

  # Check what tickers are available, as well as metadata about each ticker
  # including supported currency, exchange, and available start/end dates.
  tickers = client.list_stock_tickers()

  # Get news articles about given tickers or search terms from given domains
  articles = client.get_news(tickers=['GOOGL', 'AAPL'],
                              tags=['Laptops'],
                              sources=['washingtonpost.com'],
                              startDate='2017-01-01',
                              endDate='2017-08-31')

  # Get definitions for fields available in the fundamentals-api, ticker is
  # optional
  definitions = client.get_fundamentals_definitions('GOOGL')

  # Get fundamentals which require daily-updated (like marketCap). A start-
  # and end-date can be passed. If omited, will get all available data.
  fundamentals_daily = client.get_fundamentals_daily('GOOGL',
                                          startDate='2020-01-01',
                                          endDate='2020-12-31')

  # Get fundamentals based on quarterly statements. Accepts time-range like
  # daily-fundamentals. asReported can be set to get the data exactly like
  # it was reported to SEC. Set to False if you want to get data containing
  # corrections
  fundamentals_stmnts = client.get_fundamentals_statements('GOOGL',
                                                           startDate='2020-01-01',
                                                           endDate='2020-12-31',
                                                           asReported=True)


To receive results in ``pandas`` format, use the ``get_dataframe()`` method:

.. code-block:: python

  #Get a pd.DataFrame of the price history of a single symbol (default is daily):
  ticker_history = client.get_dataframe("GOOGL")

  #The method returns all of the available information on a symbol, such as open, high, low, close,
  #adjusted close, etc.  This page in the tiingo api documentation lists the available information on each
  #symbol: https://api.tiingo.com/docs/tiingo/daily#priceData.

  #Frequencies and start and end dates can be specified similarly to the json method above.

  #Get a pd.Series of only one column of the available response data by specifying one of the valid the
  #'metric_name' parameters:
  ticker_history = client.get_dataframe("GOOGL", metric_name='adjClose')

  #Get a pd.DataFrame for a list of symbols for a specified metric_name (default is adjClose if no
  #metric_name is specified):
  ticker_history = client.get_dataframe(['GOOGL', 'AAPL'],
                                        frequency='weekly',
                                        metric_name='volume',
                                        startDate='2017-01-01',
                                        endDate='2018-05-31')



You can specify any of the end of day frequencies (daily, weekly, monthly, and annually) or any intraday frequency for both the ``get_ticker_price`` and ``get_dataframe``
methods.  Weekly frequencies resample to the end of day on Friday, monthly frequencies resample to the last day of the month, and annually frequencies resample to the end of
day on 12-31 of each year.  The intraday frequencies are specified using an integer followed by "Min" or "Hour", for example "30Min" or "1Hour".

Cryptocurrency 
--------

.. code-block:: python

  # You can obtain cryptocurrency metadata using the following method.
  # NOTE: Crypto symbol MUST be encapsulated in brackets as a Python list!
  
  client.get_crypto_metadata(['BTCUSD'], fmt='json')

  #You can obtain top-of-book cryptocurrency quotes from the ``get_crypto_top_of_book()`` method.
  # NOTE: Crypto symbol MUST be encapsulated in brackets as a Python list!
  
  crypto_price = client.get_crypto_top_of_book(['BTCUSD'])``

  # You can obtain historical Cryptocurrency price quotes from the get_crypto_price_history() method.
  # NOTE: Crypto symbol MUST be encapsulated in brackets as a Python list!
  
  client.get_crypto_price_history(tickers = ['BTCUSD'], startDate='2020-12-2', 
                                  endDate='2020-12-3', resampleFreq='1Hour')


Websockets Support
--------

.. code-block:: python

    from tiingo import TiingoWebsocketClient
    
    def cb_fn(msg):

        # Example response 
        # msg = {
        #   "service":"iex" # An identifier telling you this is IEX data. 
        #   The value returned by this will correspond to the endpoint argument.
        #   
        #   # Will always return "A" meaning new price quotes. There are also H type Heartbeat msgs used to keep the connection alive
        #   "messageType":"A" # A value telling you what kind of data packet this is from our IEX feed.
        #  
        #   # see https://api.tiingo.com/documentation/websockets/iex > Response for more info
        #   "data":[] # an array containing trade information and a timestamp
        #   
        # }

        print(msg)

    subscribe = {
            'eventName':'subscribe',
            'authorization':'API_KEY_GOES_HERE',
            #see https://api.tiingo.com/documentation/websockets/iex > Request for more info
            'eventData': { 
                'thresholdLevel':5
          }
    }
    
    # any logic should be implemented in the callback function (cb_fn)
    TiingoWebsocketClient(subscribe,endpoint="iex",on_msg_cb=cb_fn)
  


Further Docs
-------------

* Official Tiingo Documentation: https://api.tiingo.com
* `tiingo-python` Documentation: https://tiingo-python.readthedocs.io.

Features
---------

* Easy programmatic access to Tiingo API
* Reuse requests session across API calls for better performance
* On most methods, pass in `fmt="object"` as a keyword to have your responses come back as `NamedTuples`, which should have a lower memory impact than regular Python dictionaries.

Roadmap:
---------

* Client-side validation of tickers
* Data validation of returned responses
* Case insensitivity for ticker names
* More documentation / code examples

Feel free to file a PR that implements any of the above items.

Related Projects:
------------------
* Riingo_ : Client for Tiingo in the R Programming Language

.. _Riingo: https://github.com/business-science/riingo

Credits
--------

* Many thanks to Rishi Singh for creating Tiingo.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
