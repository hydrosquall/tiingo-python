#
# Test setup based on https://gist.github.com/odyniec/d4ea0959d4e0ba17a980
#

import shutil, tempfile
from os import path
from unittest import TestCase
from tools.api_key_tool import remove_api_key, has_api_key

TEST_TEXT = """
interactions:
- request:
    body: null
    headers:
      Accept:
      - '*/*'
      Accept-Encoding:
      - gzip, deflate
      Authorization:
      - Token 0000000000000000000000000000000000000000
      Connection:
      - keep-alive
      Content-Type:
      - application/json
      User-Agent:
      - tiingo-python-client 0.14.0
    method: GET
    uri: https://api.tiingo.com/tiingo/daily/PG
  response:
    body:
      string: '{"name": "Procter & Gamble Company", "description": "P&G serves consumers
        around the world with one of the strongest portfolios of trusted, quality,
        leadership brands, including Always\u00ae, Ambi Pur\u00ae, Ariel\u00ae, Bounty\u00ae,
        Charmin\u00ae, Crest\u00ae, Dawn\u00ae, Downy\u00ae, Fairy\u00ae, Febreze\u00ae,
        Gain\u00ae, Gillette\u00ae, Head & Shoulders\u00ae, Lenor\u00ae, Olay\u00ae,
        Oral-B\u00ae, Pampers\u00ae, Pantene\u00ae, SK-II\u00ae, Tide\u00ae, Vicks\u00ae,
        and Whisper\u00ae. The P&G community includes operations in approximately
        70 countries worldwide.", "ticker": "PG", "exchangeCode": "NYSE", "startDate":
        "1970-01-02", "endDate": "2021-04-27"}'
    headers:
      allow:
      - GET, HEAD, OPTIONS
      content-length:
      - '666'
      content-type:
      - application/json
      date:
      - Wed, 28 Apr 2021 17:10:05 GMT
      server:
      - nginx/1.14.0 (Ubuntu)
      vary:
      - Accept, Cookie, Origin
      x-frame-options:
      - SAMEORIGIN
    status:
      code: 200
      message: OK
version: 1
"""


class TestAPIKeyTools(TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        f = open(path.join(self.test_dir, 'test.yaml'), 'w')
        f.write(TEST_TEXT)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_key_detector(self):
        assert has_api_key(path.join(self.test_dir, 'test.yaml')) is True

    def test_key_remover(self):
        remove_api_key(path.join(self.test_dir, 'test.yaml'))
        assert has_api_key(path.join(self.test_dir, 'test.yaml')) is False
