=======
History
=======
0.17.0 (2025-XX - Unreleased)
--------------------------------

* WIP


0.16.0 (2025-04-05)
--------------------------------

* Dev: New config for readthedocs
* Feature: Add 'columns' parameter to 'get_dataframe' and 'get_ticker_price' func (#1057)

0.15.6 (2024-05-25)
--------------------------------

* Feature: Support websockets client / endpoints (#508)
* Documentation: Add crypto endpoint examples (#621)
* Development: Code is formatted with black (#663)
* CI: Stopped testing Python versions older than 3.10 (#944)
* CI: fixed CodeCov upload (#856)
* CI: Add CodeQL for static analysis scanning (#785)
* Minor: bumped development / examples dependencies
* Minor: Switch to trusted publisher workflow

0.14.0 (2021-03-06)
--------------------------------
* Feature: Added 3 new methods for fundamentals-endpoint: definitions, daily and statements
* [/news] Fix bug in get_news() when sources list is empty (#566)
* Development: Run tests in Github Actions instead of Travis.org
* Development: This is the last version of tiingo that will support Python 3.5 and below. (#601)

0.13.0 (2020-12-12)
--------------------------------
* Minor: Address Pandas Future Warning for sorting in pd.concat (#392)
* Feature: Add option to request data in csv format in get_dataframe method potentially boosting speed up to 4-5x. (#523)
* Minor: bumped library dependencies, in particular cryptography
* Development: Dropped official support for Python 3.5, replaced with 3.7
* Development: Publish library with Github Actions instead of Travis (#546)

0.12.0 (2019-10-20)
--------------------
* Feature: Added 3 new methods for crypto endpoints: top of book prices, historical, and metadata endpoints (@n1rna #340)
* Feature: Permit list_tickers to support multiple asset types at once (@n1rna #346)

0.11.0 (2019-09-01)
--------------------
* [/news] Internally rename sources parameter to "source", ensure lists are passed as comma separated values #325. Non-breaking external change.
* [/news] Add new URL parameter for "onlyWithTickers" #327

0.10.x (2019-05-11)
--------------------
* Documentation: Added a "Peer Comparison Analysis" Jupyter Notebook under "/examples" (@i3creations #197)
* Minor: Update error message to clarify multiple tickers only work with single metrics
* Updated development dependencies

0.9.x (2019-01-30)
------------------
* Documentation: Added runnable jupyter notebook sample under "/examples"
* Minor: bumped various library dependencies

0.8.0 (2018-07-06)
------------------
* Major: Add IEX Endpoint to retrieve data with intraday frequencies (@dcwtx #125)
* Minor: update documentation for contributing/releasing new versions
* Speed up Travis build process with pip cache

0.7.0 (2018-06-14)
------------------
* Major: Provide functions for returning data as pandas Dataframes or Series (@dcwtx #112)
* Minor documentation edits

0.6.0 (2018-04-30)
------------------

* Fix bug in resample argument name (@dcwtx #82)
* Add tool for removing API Keys from test fixtures (@dcwtx #107)
* Remove official support for Python 3.3

0.5.0 (2018-03-11)
------------------

* Updated examples in docs for getting historical prices
* Add interfaces to obtain mutual fund and ETF tickers (@savagesmc #62)
* Raise explicit error when API key is missing (#44)
* Update development dependencies


0.4.0 (2017-10-22)
------------------

* Make tests run in 1/10th the time with ``vcr.py`` (@condemil #32)
* Add support for returning python objects instead of dictionaries (@BharatKalluri #33)


0.3.0 (2017-09-17)
------------------

* Add support for listing all tickers + date ranges
* Add support for interacting with the ``/news`` API
* Improve logging of REST client errors


0.2.0 (2017-09-01)
------------------

* Improve test coverage of tickers endpoint
* Deprecate the Mutual Funds endpoint

0.1.0 (2017-08-24)
------------------

* First release on PyPI.
