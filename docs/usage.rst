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

   # Get historical GOOGL prices from August 2017 as JSON, sampled daily
   historical_prices = client.get_ticker_price("GOOGL",
                                               fmt='json',
                                               startDate='2017-08-01',
                                               endDate='2017-08-31',
                                               frequency='daily')

   # Check what tickers are available, as well as metadata about each ticker
   # including supported currency, exchange, and available start/end dates.
   tickers = client.list_stock_tickers()

   # Get news articles about given tickers. Requires Pro account.
   articles = client.get_news(tickers=['GOOGL', 'APPL'], 
                              tags=['Bitcoin'], 
                              sources=['washingtonpost.com'],
                              startDate='2017-01-01',
                              endDate='2017-08-31')

Websocket support::

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
    # notice how the object isn't needed after using it
    # any logic should be implemented in the callback function 
    TiingoWebsocketClient(subscribe,endpoint="iex",on_msg_cb=cb_fn)
    while True:pass
  

Further Docs
--------

* Official Tiingo Documentation: https://api.tiingo.com
* Tiingo-Python Documentation (Under Construction): https://tiingo-python.readthedocs.io.
