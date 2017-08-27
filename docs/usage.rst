=====
Usage
=====

To use Tiingo Python in a project::

    import tiingo


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

   # To reuse the same HTTP Session across API calls (and have better)
   # performance, include a session key.
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
