#!/usr/bin/env python3

import sys
import logging

try:
    import click
except ImportError:
    print("Please install python-click")
    sys.exit(1)

from pprint import pprint
from peerplaysbase.account import PrivateKey
from peerplays.storage import configStorage as config
from peerplays.transactionbuilder import TransactionBuilder
from prettytable import PrettyTable
from .ui import (
    print_permissions,
    print_version,
)
from .decorators import (
    onlineChain,
    offlineChain,
    unlockWallet
)
from .main import main
from . import (
    account,
    info,
    proposal,
    wallet,
    witness,
    committee,
    bookie,
    message,
    rpc,
    asset,
    bos
)

log = logging.getLogger(__name__)


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
def broadcast(ctx, filename):
    if filename:
        tx = filename.read()
    else:
        tx = sys.stdin.read()
    tx = TransactionBuilder(eval(tx), peerplays_instance=ctx.peerplays)
    tx.broadcast()
    pprint(tx.json())


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
