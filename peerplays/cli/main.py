#!/usr/bin/env python3

import sys
import os
import json
import re
from pprint import pprint
import time
from peerplaysbase import transactions, operations
from peerplaysbase.account import PrivateKey, PublicKey, Address
from peerplays.storage import configStorage as config
from peerplays.peerplays import PeerPlays
from peerplays.block import Block
from peerplays.amount import Amount
from peerplays.asset import Asset
from peerplays.account import Account
from peerplays.transactionbuilder import TransactionBuilder
from prettytable import PrettyTable
import logging
from .ui import (
    print_permissions,
    get_terminal,
    pprintOperation,
    print_version,
    onlineChain,
    offlineChain,
    unlockWallet
)
from peerplays.exceptions import AccountDoesNotExistsException
from click_datetime import Datetime
from datetime import datetime

try:
    import click
except ImportError:
    print("Please install python-click")
    sys.exit(1)

log = logging.getLogger(__name__)


@click.group()
@click.option(
    '--debug/--no-debug',
    default=False,
    help="Enable/Disable Debugging (no-broadcasting mode)"
)
@click.option(
    '--node',
    type=str,
    default=config["node"],
    help='Websocket URL for public PeerPlays API'
)
@click.option(
    '--rpcuser',
    type=str,
    default=config["rpcuser"],
    help='Websocket user if authentication is required'
)
@click.option(
    '--rpcpassword',
    type=str,
    default=config["rpcpassword"],
    help='Websocket password if authentication is required')
@click.option(
    '--nobroadcast/--broadcast',
    '-d',
    default=False,
    help='Do not broadcast anything')
@click.option(
    '--unsigned/--signed',
    '-x',
    default=False,
    help='Do not try to sign the transaction')
@click.option(
    '--expires',
    '-e',
    default=30,
    help='Expiration time in seconds (defaults to 30)')
@click.option(
    '--verbose',
    '-v',
    type=int,
    default=3,
    help='Verbosity (0-15)')
@click.option(
    '--version',
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Show version")
@click.pass_context
def main(ctx, **kwargs):
    ctx.obj = {}
    for k, v in kwargs.items():
        ctx.obj[k] = v


@main.command(
    help="Set configuration key/value pair"
)
@click.pass_context
@offlineChain
@click.argument(
    'key',
    type=str
)
@click.argument(
    'value',
    type=str
)
def set(ctx, key, value):
    """ Set configuration parameters
    """
    if (key == "default_account" and
            value[0] == "@"):
        value = value[1:]
    config[key] = value


@main.command(
    help="Show configuration variables"
)
def configuration():
    t = PrettyTable(["Key", "Value"])
    t.align = "l"
    for key in config:
        if key not in [
            "encrypted_master_password"
        ]:
            t.add_row([key, config[key]])
    click.echo(t)


@main.command(
    help="Change the wallet passphrase"
)
@click.pass_context
@offlineChain
@click.option(
    '--new-password',
    prompt="New Wallet Passphrase",
    hide_input=True,
    confirmation_prompt=True,
    help="New Wallet Passphrase"
)
@unlockWallet
def changewalletpassphrase(ctx, new_password):
    ctx.peerplays.wallet.changePassphrase(new_password)


@main.command(
    help="Add a private key to the wallet"
)
@click.pass_context
@onlineChain
@click.argument(
    "key",
    nargs=-1
)
@unlockWallet
def addkey(ctx, key):
    if not key:
        while True:
            key = click.prompt(
                "Private Key (wif) [Enter to quit]",
                hide_input=True,
                show_default=False,
                default="exit"
            )
            if not key or key == "exit":
                break
            try:
                ctx.peerplays.wallet.addPrivateKey(key)
            except Exception as e:
                click.echo(str(e))
                continue

        installedKeys = ctx.peerplays.wallet.getPublicKeys()
        if len(installedKeys) == 1:
            name = ctx.peerplays.wallet.getAccountFromPublicKey(installedKeys[0])
            if name:
                account = Account(name, peerplays_instance=ctx.peerplays)
                click.echo("=" * 30)
                click.echo("Setting new default user: %s" % account["name"])
                click.echo()
                click.echo("You can change these settings with:")
                click.echo("    uptick set default_account <account>")
                click.echo("=" * 30)
                config["default_account"] = account["name"]


@main.command(
    help="Delete a private key from the wallet"
)
@click.pass_context
@offlineChain
@click.argument(
    "pubkeys",
    nargs=-1
)
def delkey(ctx, pubkeys):
    if not pubkeys:
        pubkeys = click.prompt("Public Keys").split(" ")
    if click.confirm(
        "Are you sure you want to delete keys from your wallet?\n"
        "This step is IRREVERSIBLE! If you don't have a backup, "
        "You may lose access to your account!"
    ):
        for pub in pubkeys:
            ctx.peerplays.wallet.removePrivateKeyFromPublicKey(pub)


@main.command(
    help="Obtain private key in WIF format"
)
@click.pass_context
@offlineChain
@click.argument(
    "pubkey",
    nargs=1
)
@unlockWallet
def getkey(ctx, pubkey):
    click.echo(ctx.peerplays.wallet.getPrivateKeyForPublicKey(pubkey))


@main.command(
    help="List all keys (for all networks)"
)
@click.pass_context
@offlineChain
def listkeys(ctx):
    t = PrettyTable(["Available Key"])
    t.align = "l"
    for key in ctx.peerplays.wallet.getPublicKeys():
        t.add_row([key])
    click.echo(t)


@main.command(
    help="List accounts (for the connected network)"
)
@click.pass_context
@onlineChain
def listaccounts(ctx):
    t = PrettyTable(["Name", "Type", "Available Key"])
    t.align = "l"
    for account in ctx.peerplays.wallet.getAccounts():
        t.add_row([
            account["name"] or "n/a",
            account["type"] or "n/a",
            account["pubkey"]
        ])
    click.echo(t)


@main.command(
    help="Obtain all kinds of information"
)
@click.pass_context
@onlineChain
@click.argument(
    'objects',
    type=str,
    nargs=-1
)
def info(ctx, objects):
    if not objects:
        t = PrettyTable(["Key", "Value"])
        t.align = "l"
        info = ctx.peerplays.rpc.get_dynamic_global_properties()
        for key in info:
            t.add_row([key, info[key]])
        click.echo(t.get_string(sortby="Key"))

    for obj in objects:
        # Block
        if re.match("^[0-9]*$", obj):
            block = Block(obj, peerplays_instance=ctx.peerplays)
            if block:
                t = PrettyTable(["Key", "Value"])
                t.align = "l"
                for key in sorted(block):
                    value = block[key]
                    if key == "transactions":
                        value = json.dumps(value, indent=4)
                    t.add_row([key, value])
                click.echo(t)
            else:
                click.echo("Block number %s unknown" % obj)
        # Object Id
        elif len(obj.split(".")) == 3:
            data = ctx.peerplays.rpc.get_object(obj)
            if data:
                t = PrettyTable(["Key", "Value"])
                t.align = "l"
                for key in sorted(data):
                    value = data[key]
                    if isinstance(value, dict) or isinstance(value, list):
                        value = json.dumps(value, indent=4)
                    t.add_row([key, value])
                click.echo(t)
            else:
                click.echo("Object %s unknown" % obj)

        # Asset
        elif obj.upper() == obj:
            data = Asset(obj)
            t = PrettyTable(["Key", "Value"])
            t.align = "l"
            for key in sorted(data):
                value = data[key]
                if isinstance(value, dict):
                    value = json.dumps(value, indent=4)
                t.add_row([key, value])
            click.echo(t)

        # Public Key
        elif re.match("^PPY.{48,55}$", obj):
            account = ctx.peerplays.wallet.getAccountFromPublicKey(obj)
            if account:
                t = PrettyTable(["Account"])
                t.align = "l"
                t.add_row([account])
                click.echo(t)
            else:
                click.echo("Public Key not known" % obj)

        # Account name
        elif re.match("^[a-zA-Z0-9\-\._]{2,64}$", obj):
            account = Account(obj, full=True)
            if account:
                t = PrettyTable(["Key", "Value"])
                t.align = "l"
                for key in sorted(account):
                    value = account[key]
                    if isinstance(value, dict) or isinstance(value, list):
                        value = json.dumps(value, indent=4)
                    t.add_row([key, value])
                click.echo(t)
            else:
                click.echo("Account %s unknown" % obj)
        else:
            click.echo("Couldn't identify object to read")


@main.command(
    help="Show Account balances"
)
@click.pass_context
@onlineChain
@click.argument(
    "accounts",
    nargs=-1)
def balance(ctx, accounts):
    t = PrettyTable(["Account", "Amount"])
    t.align = "r"
    for a in accounts:
        account = Account(a, peerplays_instance=ctx.peerplays)
        for b in account.balances:
            t.add_row([
                str(a),
                str(b),
            ])
    click.echo(str(t))


@main.command(
    help="Sign a json-formatted transaction"
)
@click.pass_context
@offlineChain
@click.argument(
    'filename',
    required=False,
    type=click.File('r'))
@unlockWallet
def sign(ctx, filename):
    if filename:
        tx = filename.read()
    else:
        tx = sys.stdin.read()
    tx = TransactionBuilder(eval(tx), peerplays_instance=ctx.peerplays)
    tx.appendMissingSignatures()
    tx.sign()
    pprint(tx.json())


@main.command(
    help="Broadcast a json-formatted transaction"
)
@click.pass_context
@onlineChain
@click.argument(
    'filename',
    required=False,
    type=click.File('r'))
@unlockWallet
def broadcast(ctx, filename):
    if filename:
        tx = filename.read()
    else:
        tx = sys.stdin.read()
    tx = TransactionBuilder(eval(tx), peerplays_instance=ctx.peerplays)
    tx.broadcast()
    pprint(tx.json())


@main.command(
    help="Show history of an account"
)
@click.pass_context
@onlineChain
@click.argument(
    "account",
    nargs=-1)
@click.option(
    "--csv/--table",
    help="Show output as csv or table",
    default=False)
@click.option(
    "--type",
    type=str,
    help="Only show operations of this type",
    multiple=True)
@click.option(
    "--exclude",
    type=str,
    help="Exclude certain types",
    multiple=True)
@click.option(
    "--limit",
    type=int,
    help="Limit number of elements",
    default=15)
def history(ctx, account, limit, type, csv, exclude):
    from peerplaysbase.operations import getOperationNameForId
    header = ["#", "time (block)", "operation", "details"]
    if csv:
        import csv
        t = csv.writer(sys.stdout, delimiter=";")
        t.writerow(header)
    else:
        t = PrettyTable(header)
        t.align = "r"
        t.align["details"] = "l"

    for a in account:
        account = Account(a, peerplays_instance=ctx.peerplays)
        for b in account.history(
            limit=limit,
            only_ops=type,
            exclude_ops=exclude
        ):
            row = [
                b["id"].split(".")[2],
                "%s" % (b["block_num"]),
                "{} ({})".format(getOperationNameForId(b["op"][0]), b["op"][0]),
                pprintOperation(b),
            ]
            if csv:
                t.writerow(row)
            else:
                t.add_row(row)
    if not csv:
        click.echo(t)


@main.command(
    help="Obtain a random private/public key pair"
)
@click.option(
    '--prefix',
    type=str,
    default="PPY",
    help="The refix to use"
)
@click.option(
    '--num',
    type=int,
    default=1,
    help="The number of keys to derive"
)
def randomwif(prefix, num):
    t = PrettyTable(["wif", "pubkey"])
    for n in range(0, num):
        wif = PrivateKey()
        t.add_row([
            str(wif),
            format(wif.pubkey, prefix)
        ])
    click.echo(str(t))


@main.command(
    help="Create a new account"
)
@click.pass_context
@onlineChain
@click.argument(
    "accountname",
    nargs=1,
    type=str)
@click.option(
    "--account",
    default=config["default_account"],
    help="Account to pay the registration fee"
)
@click.option(
    '--password',
    prompt="Account Password",
    hide_input=True,
    confirmation_prompt=True,
    help="Account Password"
)
@unlockWallet
def newaccount(ctx, accountname, account, password):
    pprint(ctx.peerplays.create_account(
        accountname,
        registrar=account,
        password=password,
    ))


@main.command(
    help="Transfer assets"
)
@click.pass_context
@onlineChain
@click.argument(
    "to",
    nargs=1,
    type=str)
@click.argument(
    "amount",
    nargs=1,
    type=float)
@click.argument(
    "asset",
    nargs=1,
    type=str)
@click.argument(
    "memo",
    required=False,
    type=str,
    default=None)
@click.option(
    "--account",
    default=config["default_account"],
    help="Account to send from"
)
@unlockWallet
def transfer(ctx, to, amount, asset, memo, account):
    pprint(ctx.peerplays.transfer(
        to,
        amount,
        asset,
        memo=memo,
        account=account
    ))
