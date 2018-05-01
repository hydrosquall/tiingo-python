#
# Test setup based on https://gist.github.com/odyniec/d4ea0959d4e0ba17a980
#

import shutil, tempfile
from os import path
from unittest import TestCase
from tools.api_key_tool import remove_api_key, has_api_key


class TestAPIKeyTools(TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        f = open(path.join(self.test_dir, 'test.yaml'), 'w')
        txt = '''interactions:
                    - request:
                        body: null
                        headers:
                          Accept: ['*/*']
                          Accept-Encoding: ['gzip, deflate']
                          Authorization: [Token a00000000000000000000a00000000000000000a]
                          Connection: [keep-alive]
                          Content-Type: [application/json]
                          User-Agent: [tiingo-python-client 0.5.0]
                        method: GET
                        uri: https://api.tiingo.com/tiingo/daily/GOOGL/prices?format=json&resampleFreq=daily
                      response:
                        body: {string: '[{"adjClose":1037.29,"adjHigh":1044.65,"adjLow":1026.05,"adjOpen":1031.47,"adjVolume":1644794,"close":1037.29,"date":"2018-04-12T00:00:00+00:00","divCash":0.0,"high":1044.65,"low":1026.05,"open":1031.47,"splitFactor":1.0,"volume":1644794}]'}
                        headers:
                          Allow: ['GET, HEAD, OPTIONS']
                          Content-Length: ['239']
                          Content-Type: [application/json]
                          Date: ['Fri, 13 Apr 2018 02:42:05 GMT']
                          Server: [nginx/1.10.1]
                          Vary: ['Accept, Cookie']
                          X-Frame-Options: [SAMEORIGIN]
                        status: {code: 200, message: OK}
                    version: 1
                    '''
        f.write(txt)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_key_detector(self):
        assert has_api_key(path.join(self.test_dir, 'test.yaml')) is True

    def test_key_remover(self):
        remove_api_key(path.join(self.test_dir, 'test.yaml'))
        assert has_api_key(path.join(self.test_dir, 'test.yaml')) is False
