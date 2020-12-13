============
Issuing New Releases
============

Tiingo follows semantic versioning (semver.org) practices.

The following shows how to make a release for version 0.8.0

1. Make a branch called release/0.8.0
2. Ensure HISTORY.rst (the Changelog) is up to date
3. Update __version__.py to 0.8.0 and tag the commit
4. Open a merge request to master
5. After the merge request is approved and merged, tag and push the merged commit with tag v0.8.0.
6. Visit https://github.com/hydrosquall/tiingo-python/releases and create a new release. Github Actions will deploy the new library to PyPI.
