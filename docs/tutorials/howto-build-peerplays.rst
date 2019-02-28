***********************
Building PeerPlays Node
***********************

Downloading the sources
#######################

The sources can be downloaded from::

    https://github.com/peerplays-network/peerplays

Dependencies
#############

Development Toolkit
*******************

The following dependencies were necessary for a clean install of Ubuntu 16.10:

.. code-block:: sh

    sudo apt-get update
    sudo apt-get install gcc-5 g++-5 gcc g++ cmake make \
                         libbz2-dev libdb++-dev libdb-dev \
                         libssl-dev openssl libreadline-dev \
                         autotools-dev build-essential \
                         g++ libbz2-dev libicu-dev python-dev \
                         autoconf libtool git

Boost 1.60
**********

You need to download the Boost tarball for Boost 1.60.0.

.. code-block:: sh

    export BOOST_ROOT=$HOME/opt/boost_1.60.0
    wget -c 'http://sourceforge.net/projects/boost/files/boost/1.60.0/boost_1.60.0.tar.bz2/download'\
         -O boost_1.60.0.tar.bz2
    tar xjf boost_1.60.0.tar.bz2
    cd boost_1.60.0/
    ./bootstrap.sh "--prefix=$BOOST_ROOT"
    ./b2 install

Building PeerPlays
##################

After downloading the PeerPlays sources we can run ``cmake`` for configuration
and compile with ``make``:

.. code-block:: sh

    cd peerplays
    export CC=gcc-5 CXX=g++-5
    cmake -DBOOST_ROOT="$BOOST_ROOT" -DCMAKE_BUILD_TYPE=Debug .
    make 

Note that the environmental variable ``$BOOST_ROOT`` should point to your
install directory of boost if you have installed it manually (see first line in
the previous example)

Binaries
########

After compilation, the binaries are located in::

    ./programs/witness_node
    ./programs/cli_wallet
    ./programs/delayed_node
