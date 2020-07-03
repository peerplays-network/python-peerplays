import click
from pprint import pprint
from prettytable import PrettyTable
from .decorators import onlineChain, unlockWallet, customchain
from .main import main
from .ui import pretty_print

from peerplays.account import Account
from peerplays.asset import Asset
from peerplays.sport import Sport, Sports
from peerplays.eventgroup import EventGroup, EventGroups
from peerplays.event import Event, Events
from peerplays.bettingmarketgroup import BettingMarketGroup, BettingMarketGroups
from peerplays.rule import Rule, Rules
from peerplays.proposal import Proposals


@main.group()
def rbac():
    """ RBAC related calls
    """
    pass


@rbac.command()
@click.pass_context
@click.argument("account")
@customchain(bundle=True)
# @unlockWallet
def get_custom_permissions(ctx, account):
    pprint(ctx.peerplays.rpc.get_custom_permissions(account))

@rbac.command()
@click.pass_context
@click.argument("account")
@customchain(bundle=True)
# @unlockWallet
def get_custom_account_authorities(ctx, account):
    pprint(ctx.peerplays.rpc.get_custom_account_authorities(account))

@rbac.command()
@click.pass_context
@click.argument("account")
@customchain(bundle=True)
@unlockWallet
def custom_permission_create(ctx, account):
    pass


