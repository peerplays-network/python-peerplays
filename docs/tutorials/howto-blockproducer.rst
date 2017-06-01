*****************************************
Setup a witness and block producing node
*****************************************

After :doc:`having setup a node <howto-trusted-node>`, we can setup a
witness and block producing node. We will need:

* A compiled ``witness_node``
* A compiled ``cli_wallet``
* A registered account
* The active private key to that account
* Some little funds to pay for witness registration in your account

Lunching the cli_wallet
=======================

We first need to launch the cli_wallet and setup a local wallet with it:::

    ./programs/cli_wallet/cli_wallet --server-rpc-endpoint wss://node-to-some-public-api-node

First thing to do is setting up a password for the newly created wallet prior to
importing any private keys:::

    >>> set_password <password>
    null
    >>> unlock <password>
    null
    >>>

Basic Account Management
========================

We can import your account with::

    >>> import_key <accountname> <active wif key>
    true
    >>> list_my_accounts
    [{
    "id": "1.2.15",
    ...
    "name": <accountname>,
    ...
    ]
    >>> list_account_balances <accountname>
    XXXXXXX PPY

Registering a Witness
=====================

To become a witness and be able to produce blocks, you first need to create a
witness object that can be voted in.

We create a new witness by issuing:::

    >>> create_witness <accountname> "http://<url-to-proposal>" true
    {
      "ref_block_num": 139,
      "ref_block_prefix": 3692461913,
      "relative_expiration": 3,
      "operations": [[
      21,{
        "fee": {
          "amount": 0,
          "asset_id": "1.3.0"
        },
        "witness_account": "1.2.16",
        "url": "url-to-proposal",
        "block_signing_key": "<PUBLIC KEY>",
        "initial_secret": "00000000000000000000000000000000000000000000000000000000"
      }
    ]
      ],
      "signatures": [
      "1f2ad5597af2ac4bf7a50f1eef2db49c9c0f7616718776624c2c09a2dd72a0c53a26e8c2bc928f783624c4632924330fc03f08345c8f40b9790efa2e4157184a37"
      ]
    }

The cli_wallet will create a new public key for signing ``<PUBLIC
KEY>``. We now need to obtain the private key for that:::

    get_private_key <PUBLIC KEY>


Configuration of the Witness Node
=================================

Get the witness object using::

    get_witness <witness-account>
    
and take note of two things. The ``id`` is displayed in ``get_global_properties``
when the witness is voted in, and we will need it on the ``witness_node`` command
line to produce blocks. We'll also need the public ``signing_key`` so we can
look up the correspoinding private key.

.. code-block:: sh

    >>> get_witness <accountname>
    {
      [...]
      "id": "1.6.10",
      "signing_key": "GPH7vQ7GmRSJfDHxKdBmWMeDMFENpmHWKn99J457BNApiX1T5TNM8",
      [...]
    }

The ``id`` and the ``signing_key`` are the two important parameters, here. Let's get
the private key for that signing key with:::

    get_private_key <PUBLIC KEY>

Now we need to start the witness, so shut down the wallet (ctrl-d),  and shut
down the witness (ctrl-c).  Re-launch the witness, now mentioning the new
witness 1.6.10 and its keypair:::

    ./witness_node --rpc-endpoint=127.0.0.1:8090 \
                   --witness-id '"1.6.10"' \
                   --private-key '["GPH7vQ7GmRSJfDHxKdBmWMeDMFENpmHWKn99J457BNApiX1T5TNM8", "5JGi7DM7J8fSTizZ4D9roNgd8dUc5pirUe9taxYCUUsnvQ4zCaQ"]'

Alternatively, you can also add this line into yout config.ini:::

    witness-id = "1.6.10"
    private-key = ["GPH7vQ7GmRSJfDHxKdBmWMeDMFENpmHWKn99J457BNApiX1T5TNM8","5JGi7DM7J8fSTizZ4D9roNgd8dUc5pirUe9taxYCUUsnvQ4zCaQ"]

.. note:: Make sure to use YOUR public/private keys instead of the once given
          above!

Verifying Block Production
##########################

If you monitor the output of the `witness_node`, you should see it generate 
blocks signed by your witness:::

    Witness 1.6.10 production slot has arrived; generating a block now...
    Generated block #367 with timestamp 2015-07-05T20:46:30 at time 2015-07-05T20:46:30
