# Python Library for PeerPlays

<!-- EXCLUDE_FROM_PYPI -->
### Master:

[![docs master](https://readthedocs.org/projects/python-peerplays/badge/?version=master)](http://python-peerplays.readthedocs.io/en/latest/)
[![Build Status](https://travis-ci.org/PBSA/python-peerplays.svg?branch=master)](https://travis-ci.org/PBSA/python-peerplays)
[![codecov](https://codecov.io/gh/pbsa/python-peerplays/branch/master/graph/badge.svg)](https://codecov.io/gh/pbsa/python-peerplays)

### Develop:

[![docs master](https://readthedocs.org/projects/python-peerplays/badge/?version=develop)](http://python-peerplays.readthedocs.io/en/latest/)
[![Build Status](https://travis-ci.org/PBSA/python-peerplays.svg?branch=develop)](https://travis-ci.org/PBSA/python-peerplays)
[![codecov](https://codecov.io/gh/pbsa/python-peerplays/branch/develop/graph/badge.svg)](https://codecov.io/gh/pbsa/python-peerplays)
<!-- END_EXCLUDE_FROM_PYPI -->

This is a communications library which allows interface with the Peerplays blockchain directly and without the need for a cli_wallet. It provides a wallet interface and can construct any kind of transactions and properly sign them for broadcast.

When installed with pip3, also provides a command-line interface invocable at the command line as `peerplays`.

## Installation

The python-peerplays library has following dependencies
  python3-dev
  build-essential
  libssl-dev
  libffi-dev
  libxml2-dev
  libxslt1-dev
  zlib1g-dev

Make sure that the above dependencies are installed, if not install with:

    $ sudo apt-get install <dependency name>

Install with `pip3`:

    $ pip3 install peerplays

