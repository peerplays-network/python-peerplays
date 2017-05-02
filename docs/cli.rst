*****************************
"peerplays" command line tool
*****************************

The ``peerplays`` command line tool comes with the following features:

.. code-block:: console

    $ peerplays --help
    Usage: peerplays [OPTIONS] COMMAND [ARGS]...

    Options:
      --debug / --no-debug            Enable/Disable Debugging (no-broadcasting
                                      mode)
      --node TEXT                     Websocket URL for public Peerplays API
                                      (default: "wss://t.b.d./")
      --rpcuser TEXT                  Websocket user if authentication is required
      --rpcpassword TEXT              Websocket password if authentication is
                                      required
      -d, --nobroadcast / --broadcast
                                      Do not broadcast anything
      -x, --unsigned / --signed       Do not try to sign the transaction
      -e, --expires INTEGER           Expiration time in seconds (defaults to 30)
      -v, --verbose INTEGER           Verbosity (0-15)
      --version                       Show version
      --help                          Show this message and exit.

    Commands:
      addkey                  Add a private key to the wallet
      allow                   Add a key/account to an account's permission
      approvecommittee        Approve committee member(s)
      approveproposal         Approve a proposal
      approvewitness          Approve witness(es)
      balance                 Show Account balances
      broadcast               Broadcast a json-formatted transaction
      changewalletpassphrase  Change the wallet passphrase
      configuration           Show configuration variables
      delkey                  Delete a private key from the wallet
      disallow                Remove a key/account from an account's...
      disapprovecommittee     Disapprove committee member(s)
      disapproveproposal      Disapprove a proposal
      disapprovewitness       Disapprove witness(es)
      getkey                  Obtain private key in WIF format
      history                 Show history of an account
      info                    Obtain all kinds of information
      listaccounts            List accounts (for the connected network)
      listkeys                List all keys (for all networks)
      newaccount              Create a new account
      permissions             Show permissions of an account
      randomwif               Obtain a random private/public key pair
      set                     Set configuration key/value pair
      sign                    Sign a json-formatted transaction
      transfer                Transfer assets
      upgrade                 Upgrade Account

Further help can be obtained via:

.. code-block:: console

    $ peerplays <command> --help
