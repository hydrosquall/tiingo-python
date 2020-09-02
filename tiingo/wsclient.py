import os
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
import json

GLOB_config=None
GLOB_on_msg_cb=None

class genericWebsocketClient:
    '''
    the methods passed to websocketClient have to be unbounded if we want WebSocketApp to pass everything correctly
    see websocket-client/#471
    '''
    def on_message(ws, message):
        GLOB_on_msg_cb(message)
    def on_error(ws, error):
        print(error)
    def on_close(ws):
        pass
    def on_open(ws):
        def run(*args):
            print(GLOB_config)
            ws.send(json.dumps(GLOB_config))
        thread.start_new_thread(run, ())
    def __init__(self,config,on_msg_cb):
        global GLOB_config
        global GLOB_on_msg_cb
        GLOB_config=config
        GLOB_on_msg_cb=on_msg_cb
        return

class TiingoWebsocketClient:
    '''
    from tiingo import TiingoWebsocketClient
    def cb_fn(msg):
        print(msg)
    subscribe = {
            'eventName':'subscribe',
            'authorization':'API_KEY_GOES_HERE',
            'eventData': {
                'thresholdLevel':5
          }
    }
    client=TiingoWebsocketClient(subscribe,endpoint="iex",on_msg_cb=cb_fn)
    while True:pass
    '''

    def __init__(self,config={},endpoint=None,on_msg_cb=None):
        
        self._base_url = "wss://api.tiingo.com"
        self.config=config
        
        try:
            api_key = self.config['authorization']
        except KeyError:
            api_key = os.environ.get('TIINGO_API_KEY')
            self.config.update({"authorization":api_key})

        self._api_key = api_key
        if not(api_key):
            raise RuntimeError("Tiingo API Key not provided. Please provide"
                               " via environment variable or config argument."
                               "Notice that this config dict ticks the API Key as authorization ")

        try:
            self.endpoint = endpoint
            if self.endpoint==None:
                raise KeyError
            if not (self.endpoint=="iex" or self.endpoint=="fx" or self.endpoint=="crypto"):
                raise KeyError
        except KeyError:
            raise AttributeError("Endpoint must be defined as either (iex,fx,crypto) ")
        
        self.on_msg_cb = on_msg_cb
        if self.on_msg_cb==None:
            raise AttributeError("please define on_msg_cb ")

        ws_client = genericWebsocketClient(config=self.config,on_msg_cb=self.on_msg_cb)
        

        websocket.enableTrace(True)
        
        ws = websocket.WebSocketApp("{0}/{1}".format(self._base_url,self.endpoint),
                              on_message = genericWebsocketClient.on_message,
                              on_error = genericWebsocketClient.on_error,
                              on_close = genericWebsocketClient.on_close,
                              on_open = genericWebsocketClient.on_open)
        ws.run_forever()

