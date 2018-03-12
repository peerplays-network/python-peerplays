import click
from pprint import pprint
from .decorators import (
    onlineChain,
)
from .main import main


@main.command()
@click.pass_context
@onlineChain
@click.argument(
    'call',
    nargs=1)
@click.argument(
    'arguments',
    nargs=-1)
@click.option(
    "--api",
    default="database",
    help="Provide API node, if not 'database'",
    type=str)
def rpc(ctx, call, arguments, api):
    """ Construct RPC call directly
        \b
        You can specify which API to send the call to:

            peerplays rpc --api bookie get_matched_bets_for_bettor 1.2.0

        You can also specify lists using

            peerplays rpc get_objects "['2.0.0', '2.1.0']"

    """
    try:
        data = list(eval(d) for d in arguments)
    except:
        data = arguments
    ret = getattr(ctx.peerplays.rpc, call)(*data, api=api)
    pprint(ret)
