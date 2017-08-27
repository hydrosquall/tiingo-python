=====
Usage
=====

To use Tiingo Python in a project::

    import tiingo

Now you can use the ``TiingoClient`` to make your API calls. (Other parameters are available for each endpoint beyond what has been written below, see docs for full details.)

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
