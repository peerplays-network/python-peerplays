***************************************************
Howto Monitor the blockchain for certain operations
***************************************************

Block Structure
===============

A block takes the following form:

.. code-block:: js

     {'extensions': [],
      'previous': '000583428a021b14c02f0faaff12a4c686e475e3',
      'timestamp': '2017-04-21T08:38:35',
      'transaction_merkle_root': '328be3287f89aa4d21c69cb617c4fcc372465493',
      'transactions': [{'expiration': '2017-04-21T08:39:03',
                        'extensions': [],
                        'operation_results': [[0, {}]],
                        'operations': [
                            [0,
                                {'amount': {'amount': 100000,
                                            'asset_id': '1.3.0'},
                                 'extensions': [],
                                 'fee': {'amount': 2089843,
                                         'asset_id': '1.3.0'},
                                 'from': '1.2.18',
                                 'memo': {'from': 'PPY1894jUspGi6fZwnUmaeCPDZpke6m4T9bHtKrd966M7qYz665xjr',
                                          'message': '5d09c06c4794f9bcdef9d269774209be',
                                          'nonce': '7364013452905740719',
                                          'to': 'PPY16MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV'},
                                 'to': '1.2.6'}]
                        ],
                        'ref_block_num': 33602,
                        'ref_block_prefix': 337314442,
                        'signatures': ['1f3755deaa7f9........']}],
      'witness': '1.6.4',
      'witness_signature': '2052571f091c4542...........'}

Please note that a block can **carry multiple transactions** while each
transaction **carries multiple operations**. Each operation could be a
**transfer**, or any other type of operation from a list of available
operations. Technically, an operation could be seen as a smart contract
that comes with operation-specific side-information and results in some
changes in the blockchain database.

In the example above, the operation type is identified by the ``0``,
which makes it a ``transfer`` and the structure afterwards carries the
transfer-specific side information, e.g. ``from``, ``to`` accounts,
``fee`` aswell as the ``memo``.


Polling Approach
================

Blocks can be polled with as little code as this:

.. code-block:: python

    from peerplays.blockchain import Blockchain
    chain = Blockchain()
    for block in chain.blocks(start=START_BLOCK):
        print(block)

.. note:: ``chain.blocks()`` is a blocking call that will wait for new
          blocks and yield them to the for loop when they arrive.

Alternatively, one can construct a loop that only yields the operations
on the blockchain and does not show the block structure:

.. code-block:: python

    from peerplays.blockchain import Blockchain
    chain = Blockchain()
    for op in chain.ops(start=START_BLOCK):  # Note the `ops`
        print(op)

If you are only interested in transfers, you may want to use this
instead:

.. code-block:: python

    from peerplays.blockchain import Blockchain
    chain = Blockchain()
    for transfer in chain.stream(opNames=["transfer"], start=START_BLOCK):  # Note the `ops`
       print(transfer)


.. warning:: By default, the ``Blockchain()`` instance will only look at
             **irrversible** blocks, this means that blocks are only
             considered if they are approved/signed by a majority of the
             witnesses and this lacks behind the head block by a short
             period of time (in the seconds to low minutes).

Notification Approach
=====================

*under construction*
