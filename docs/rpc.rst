**********************
Remote Procedure Calls
**********************

Prerequisits
############

This page assumes that you either have a full node or a wallet running and
listening to port ``8090``, locally.

.. note:: The set of available commands depends on application you connect to.

Call Format
###########

In Graphene, RPC calls are state-less and accessible via regular JSON formated
RPC-HTTP-calls. The correct structure of the JSON call is

.. code-block:: js

    {
     "jsonrpc": "2.0",
     "id": 1
     "method": "get_accounts",
     "params": [["1.2.0", "1.2.1"]],
    }

The ``get_accounts`` call is available in the Full Node's ``database`` API and
takes only one argument which is an array of account ids (here: ``["1.2.0", "1.2.1"]``).

Example Call with `curl`
------------------------

Such as call can be submitted via ``curl``:

.. code-block:: sh

    curl --data '{"jsonrpc":"2.0","method":"call", "params":[0, "get_accounts", [["1.2.0", "1.2.1"]]],"id":0}' https://ppy-node.bitshares.eu


Successful Calls
----------------

The API will return a properly JSON formated response carrying the same ``id``
as the request to distinguish subsequent calls.

.. code-block:: js

    {
     "id":1,
     "result":  ..data..
    }

Errors
------

In case of an error, the resulting answer will carry an ``error`` attribute and
a detailed description:

.. code-block:: js

    {
      "id": 0
      "error": {
        "data": {
          "code": error-code,
          "name": " .. name of exception .."
          "message": " .. message of exception ..",
          "stack": [ .. stack trace .. ],
        },
        "code": 1,
      },
    }

Remarks
#######

Wallet specific commands, such as ``transfer`` and market orders, are only
available if connecting to ``cli_wallet`` because only the wallet has the
private keys and signing capabilities and some calls will only execute of the
wallet is unlocked.

The full node offers a set of API(s), of which only the ``database`` calls are
avaiable via RPC. Calls that are restricted by default (i.e.
``network_node_api``) or have been restricted by configuration are not
accessible via RPC because a statefull protocol (websocket) is required for
login.
