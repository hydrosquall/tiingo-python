from unittest import TestCase
from tiingo.wsclient import TiingoWebsocketClient
from tiingo.exceptions import MissingRequiredArgumentError

class TestRestClientWithSession(TestCase):
    def setUp(self):

        def msg_cb(msg):
            print(msg)

        self.cb=msg_cb

        self.config =  {
            'eventName':'subscribe',
            'authorization':'API_KEY_GOES_HERE',
            #see https://api.tiingo.com/documentation/websockets/iex > Request for more info
            'eventData': { 
                'thresholdLevel':5
            }
        }

    # test for missing or incorrectly supplied endpoints
    def test_missing_or_wrong_endpoint(self):
        with self.assertRaises(AttributeError) as ex:
            TiingoWebsocketClient(config=self.config,on_msg_cb=self.cb)
        self.assertTrue(type(ex.exception)==AttributeError)

        with self.assertRaises(AttributeError) as ex:
             TiingoWebsocketClient(config=self.config,endpoint='wq',on_msg_cb=self.cb)
        self.assertTrue(type(ex.exception)==AttributeError)

    # test for missing API keys in config dict
    def test_missing_api_key(self):
        with self.assertRaises(RuntimeError) as ex:
            TiingoWebsocketClient(config={},endpoint='iex',on_msg_cb=self.cb)
        self.assertTrue(type(ex.exception)==RuntimeError)

    # test for missing callback argument    
    def test_missing_msg_cb(self):
        with self.assertRaises(MissingRequiredArgumentError) as ex:
            TiingoWebsocketClient(config=self.config,endpoint='iex')
        self.assertTrue(type(ex.exception)==MissingRequiredArgumentError)