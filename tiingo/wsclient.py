import os
import websocket
import json
from tiingo.exceptions import MissingRequiredArgumentError


class TiingoWebsocketClient:
    """
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
    """

    def __init__(self, config=None, endpoint=None, on_msg_cb=None):
        self._base_url = "wss://api.tiingo.com"
        self.config = {} if config is None else config

        try:
            api_key = self.config["authorization"]
        except KeyError:
            api_key = os.environ.get("TIINGO_API_KEY")
            self.config.update({"authorization": api_key})

        self._api_key = api_key
        if not (api_key):
            raise RuntimeError(
                "Tiingo API Key not provided. Please provide"
                " via environment variable or config argument."
                "Notice that this config dict takes the API Key as authorization "
            )

        self.endpoint = endpoint
        if not (
            self.endpoint == "iex" or self.endpoint == "fx" or self.endpoint == "crypto"
        ):
            raise AttributeError("Endpoint must be defined as either (iex,fx,crypto) ")

        self.on_msg_cb = on_msg_cb
        if not self.on_msg_cb:
            raise MissingRequiredArgumentError(
                "please define on_msg_cb It's a callback that gets called when new messages arrive "
                "Example:"
                "def cb_fn(msg):"
                "    print(msg)"
            )

        websocket.enableTrace(False)

        ws = websocket.WebSocketApp(
            "{0}/{1}".format(self._base_url, self.endpoint),
            on_message=self.get_on_msg_cb(),
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.get_on_open(self.config),
        )
        ws.run_forever()

    def get_on_open(self, config):
        # the methods passed to websocketClient have to be unbounded if we want WebSocketApp to pass everything correctly
        # see websocket-client/#471
        def on_open(ws):
            ws.send(json.dumps(config))

        return on_open

    def get_on_msg_cb(self):
        def on_msg_cb_local(ws, msg):
            self.on_msg_cb(msg)
            return

        return on_msg_cb_local

    # since methods need to be unbound in order for websocketClient these methods don't have a self as their first parameter
    def on_error(ws, error):  # lgtm[py/not-named-self]
        print(error)

    def on_close(ws):  # lgtm[py/not-named-self]
        pass
