*****************************************
Trusted Network and Client Configuration
*****************************************

Introduction
____________________

Similar to other crypto currencies, it is recommended to wait for several
confirmations of a transcation. Even though the consensus scheme of Graphene is
alot more secure than regular proof-of-work or other proof-of-stake schemes, we
still support exchanges that require more confirmations for deposits.

We provide a so called *delayed* full node which accepts two additional
parameters for the configuration besides those already available with the
standard daemon.

* `trusted-node` RPC endpoint of a trusted validating node (required)

The trusted-node is a regular full node directly connected to the P2P
network that works as a proxy. The delay between the trusted node and
the delayed node is chosen automatically in a way that ensures that
blocks that are available in the delayed node are guarenteed to be
**irreversible**. Thus, the delayed full node will be behind the real
blockchain by a few seconds up to only a few minutes.

.. note:: **Irrversibility**: On DPOS chains, blocks are irreversible if
          it has been approved/confirmed by at least 2/3 of all block
          validators (i.e. witnesses)

Overview of the Setup
-------------------------------

In the following, we will setup and use the following network:::

    P2P network <-> Trusted Full Node <-> Delayed Full Node <-> API

* P2P network:
  The PeerPlays client uses a peer-to-peer network to connect and broadcasts
  transactions there. A block producing full node will eventually catch your
  transcaction and validate it by adding it into a new block.
* Trusted Full Node:
  We will use a Full node to connect to the network directly. We call it
  *trusted* since it is supposed to be under our control.
* Delayed Full Node:
  The delayed full node node will provide us with a delayed and several times
  confirmed and verified blockchain. Even though DPOS is more resistant against
  forks than most other blockchain consensus schemes, we delay the blockchain
  here to reduces the risk of forks even more. In the end, the delayed full
  node is supposed to never enter an invalid fork.
* API:
  Since we have a delayed full node that we can fully trust, we will interface
  with this node to query the blockchain and receive notifications from it once
  balance changes.

The delayed full node should be in the same *local* network as the trusted full
node, however only the trusted full node requires public internet access. Hence we will work with
the following IPs:

* Trusted Full Node:
   * extern: *internet access*
   * intern: `192.168.0.100`

* Delayed Full Node:
   * extern: *no* internet access required
   * intern: `192.168.0.101`

Let's go into more detail on how to set these up.

Trusted Full Node
_________________

For the trusted full node, the default settings can be used.  Later, we
will need to open the RPC port and listen to an IP address to connect the
delayed full node to::

    ./programs/witness_node/witness_node --rpc-endpoint="192.168.0.100:8090"

.. note:: A *witness* node is identical to a full node if no authorized
          block-signing private key is provided.

Delayed Full Node
_________________

The delayed full node will need the IP address and port of the p2p-endpoint
from the trusted full node and the number of blocks that should be delayed.  We
also need to open the RPC/Websocket port (to the local network!) so that we can
interface using RPC-JSON calls.

For our example and for 10 blocks delayed (i.e. 30 seconds for 3 second block
intervals), we need:::

    ./programs/delayed_node/delayed_node --trusted-node="192.168.0.100:8090" --rpc-endpoint="192.168.0.101:8090"

We can now connect via RPC:

* `192.168.0.100:8090` : The trusted full node exposed to the internet
* `192.168.0.101:8090` : The delayed full node not exposed to the internet

.. note:: For security reasons, an exchange should only interface with the delayed
          full node.

For obvious reasons, the trusted full node is should be running before
attempting to start the delayed full node.
