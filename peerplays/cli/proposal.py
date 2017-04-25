import click
from pprint import pprint
from peerplays.storage import configStorage as config
from .decorators import (
    onlineChain,
    unlockWallet
)
from .main import main


@main.command()
@click.pass_context
@onlineChain
@click.argument(
    'proposal',
    nargs=-1)
@click.option(
    "--account",
    help="Account that takes this action",
    default=config["default_account"],
    type=str)
@unlockWallet
def disapproveproposal(ctx, proposal, account):
    """ Disapprove a proposal
    """
    pprint(ctx.peerplays.disapproveproposal(
        proposal,
        account=account
    ))


@main.command()
@click.pass_context
@onlineChain
@click.argument(
    'proposal',
    nargs=-1)
@click.option(
    "--account",
    help="Account that takes this action",
    default=config["default_account"],
    type=str)
@unlockWallet
def approveproposal(ctx, proposal, account):
    """ Approve a proposal
    """
    pprint(ctx.peerplays.approveproposal(
        proposal,
        account=account
    ))
