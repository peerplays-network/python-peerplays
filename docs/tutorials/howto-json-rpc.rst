**********************************
Interfacing via RPC and Websockets
**********************************

Overview
========

APIs are separated into two categories, namely

* the **Blockchain API** which is used to query blockchain data (account, assets, trading history, etc.) and 
* the **CLI Wallet API** which has your private keys loaded and is required when interacting with the blockchain with new transactions.

Blockchain API
--------------

The blockchain API (as provided by the ``witness_node`` application),
allows to read the blockchain.

.. code-block:: python

    from peerplaysapi.node import PeerPlaysNodeRPC
    ppy = PeerPlaysNodeRPC("wss://hostname")
    print(ppy.get_account_by_name("init0"))
    print(ppy.get_block(1))


.. note:: It is important to understand that the blockchain API does not
          know about private keys, and cannot sign transactions for you.
          All it does is validate and broadcast transactions to the P2P
          network.

CLI Wallet API
--------------

The cli-wallet api, as provided by the ``cli_wallet`` binary, allows to
**create and sign transactions** and broadcast them.

.. code-block:: python

   from peerplaysapi.wallet import PeerPlaysWalletRPC
   rpc = PeerPlaysWalletRPC("localhost", 8090)
   print(rpc.info())
