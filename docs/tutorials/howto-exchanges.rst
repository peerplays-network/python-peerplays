Howto Interface your Exchange with PeerPlays
============================================

This Howto serves as an introduction for exchanges that want to
interface with PeerPlays to allow trading of assets from the PeerPlays
network.

We here start by introducing the overall concept of trusted node setup,
having different APIs that reply in JSON and describe the structure of
the received information (blocks etc).

Afterwards, we will go into more detail w.r.t. to the python-peerplays
library that helps you deal with the blockchain and can be seen as a
full-featured wallet (to replace the cli-wallet).

.. toctree::

   howto-build-peerplays.rst
   howto-trusted-node
   ../rpc
   howto-json-rpc
   howto-monitor-blocks
   howto-decode-memo
