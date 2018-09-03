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
from peerplays.storage import configStorage as config


@main.group()
def bos():
    """ BOS related calls
    """
    pass


@bos.command()
@click.pass_context
@click.argument(
    "eventids",
    nargs=-1)
@customchain(bundle=True)
@unlockWallet
def cancel_event(ctx, eventids):
    for eventid in eventids:
        Event(eventid)
        ctx.blockchain.event_update_status(
            eventid,
            "canceled",
        )
    click.echo(ctx.broadcast())


@bos.command()
@click.pass_context
@click.argument("account")
@onlineChain
@unlockWallet
def approve_all(ctx, account):
    proposals = Proposals(account)
    proposal_ids = {x["id"] for x in proposals}
    click.echo(ctx.peerplays.approveproposal(
        proposal_ids,
        account=account
    ))
