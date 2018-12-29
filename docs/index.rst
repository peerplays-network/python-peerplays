.. python-peerplays documentation master file, created by
   sphinx-quickstart on Fri Jun  5 14:06:38 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. http://sphinx-doc.org/rest.html
   http://sphinx-doc.org/markup/index.html
   http://sphinx-doc.org/markup/para.html
   http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/rest_syntax.html
   http://rest-sphinx-memo.readthedocs.org/en/latest/ReST.html

Welcome to pypeerplays's documentation!
===============================================

PeerPlays is a **blockchain-based autonomous company** (i.e. a DAC) that
offers gaming and tournaments on a blockchain.

It is based on *Graphene* (tm), a blockchain technology stack (i.e.
software) that allows for fast transactions and a scalable blockchain
solution. In case of PeerPlays, it comes with decentralized gaming
engine and allows setting up and running tournaments of any kind.

About this Library
------------------

The purpose of *pypeerplays* is to simplify development of products and
services that use the PeerPlays blockchain. It comes with

* it's own (bip32-encrypted) wallet
* RPC interface for the Blockchain backend
* JSON-based blockchain objects (accounts, blocks, events, etc)
* a simple to use yet powerful API
* transaction construction and signing
* push notification API
* *and more*

Quickstart
----------

.. note:: All methods that construct and sign a transaction can be given
          the ``account=`` parameter to identify the user that is going
          to affected by this transaction, e.g.:
          
          * the source account in a transfer
          * the accout that buys/sells an asset in the exchange
          * the account whos collateral will be modified

         **Important**, If no ``account`` is given, then the
         ``default_account`` according to the settings in ``config`` is
         used instead.

.. code-block:: python

   from peerplays import PeerPlays
   peerplays = PeerPlays()
   peerplays.wallet.unlock("wallet-passphrase")
   peerplays.transfer("<to>", "<amount>", "<asset>", ["<memo>"], account="<from>")

.. code-block:: python

   from peerplays.blockchain import Blockchain
   blockchain = Blockchain()
   for op in Blockchain.ops():
       print(op)

.. code-block:: python

   from peerplays.block import Block
   print(Block(1))

.. code-block:: python

   from peerplays.account import Account
   account = Account("init0")
   print(account.balances)
   print(account.openorders)
   for h in account.history():
       print(h)


General
-------------------------
.. toctree::
   :maxdepth: 1

   installation
   quickstart
   tutorials
   contribute
   support
   stati

Command Line Tool
-----------------

.. toctree::
   :maxdepth: 1

   cli

Packages
--------

peerplays
~~~~~~~~~

.. toctree::
   :maxdepth: 3

   peerplays

peerplaysbase
~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 3

   peerplaysbase

Tutorials
---------

.. toctree::
   :maxdepth: 2

   tutorials/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
