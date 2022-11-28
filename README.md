# Python Library for PeerPlays

## Master:

[![docs master](https://readthedocs.org/projects/python-peerplays/badge/?version=master)](http://python-peerplays.readthedocs.io/en/latest/)
[![Build Status](https://travis-ci.org/PBSA/python-peerplays.svg?branch=master)](https://travis-ci.org/PBSA/python-peerplays)
[![codecov](https://codecov.io/gh/pbsa/python-peerplays/branch/master/graph/badge.svg)](https://codecov.io/gh/pbsa/python-peerplays)

## Develop:

[![docs master](https://readthedocs.org/projects/python-peerplays/badge/?version=develop)](http://python-peerplays.readthedocs.io/en/latest/)
[![Build Status](https://travis-ci.org/PBSA/python-peerplays.svg?branch=develop)](https://travis-ci.org/PBSA/python-peerplays)
[![codecov](https://codecov.io/gh/pbsa/python-peerplays/branch/develop/graph/badge.svg)](https://codecov.io/gh/pbsa/python-peerplays)

This is a communications library which allows interface with the Peerplays blockchain directly and without the need for a cli_wallet. It provides a wallet interface and can construct any kind of transactions and properly sign them for broadcast.

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
    
Starting cli_wallet server :

	  $ ./cli_wallet -s "ws://10.11.12.101:8090" --chain-id "7c1c72eb738b3ff1870350f85daca27e2d0f5dd25af27df7475fbd92815e421e" -r "0.0.0.0:8091"

        This starts a cli_wallet server endpoint in the local machine at port 8091

Example
    $ ./cli_wallet -s "ws://10.11.12.101:8090" --chain-id "7c1c72eb738b3ff1870350f85daca27e2d0f5dd25af27df7475fbd92815e421e" -r "0.0.0.0:8091" 


Example call
	$ curl --silent --data '{"jsonrpc": "2.0", "method": "info", "params": [], "id": 1}' http://0.0.0.0:8091 | jq

    

