import click
from pprint import pprint
from prettytable import PrettyTable
from .decorators import onlineChain
from .main import main
from .ui import pretty_print

from peerplays.asset import Asset
from peerplays.sport import Sport, Sports
from peerplays.eventgroup import EventGroup, EventGroups
from peerplays.event import Event, Events
from peerplays.bettingmarketgroup import BettingMarketGroup, BettingMarketGroups
from peerplays.rule import Rule, Rules


@main.group()
def bookie():
    """ Bookie related calls
    """
    pass


@bookie.command()
@click.pass_context
@onlineChain
def sports(ctx):
    """ [bookie] List sports """
    sports = Sports(peerplays_instance=ctx.peerplays)
    click.echo(pretty_print(sports, ctx=ctx))


@bookie.command()
@click.argument("sport")
@click.pass_context
@onlineChain
def eventgroups(ctx, sport):
    """ [bookie] List event groups for a sport

        :param str sport: Sports id
    """
    sport = Sport(sport, peerplays_instance=ctx.peerplays)
    click.echo(pretty_print(sport.eventgroups, ctx=ctx))


@bookie.command()
@click.argument("eventgroup")
@click.pass_context
@onlineChain
def events(ctx, eventgroup):
    """ [bookie] List events for an event group

        :param str eventgroup: Event Group id
    """
    eg = EventGroup(eventgroup, peerplays_instance=ctx.peerplays)
    click.echo(pretty_print(eg.events, ctx=ctx))


@bookie.command()
@click.argument("event")
@click.pass_context
@onlineChain
def bmgs(ctx, event):
    """ [bookie] List betting market groups for an event

        :param str event: Event id
    """
    eg = Event(event, peerplays_instance=ctx.peerplays)
    click.echo(pretty_print(eg.bettingmarketgroups, ctx=ctx))


@bookie.command()
@click.argument("bmg")
@click.pass_context
@onlineChain
def bettingmarkets(ctx, bmg):
    """ [bookie] List betting markets for bmg

        :param str bmg: Betting market id
    """
    bmg = BettingMarketGroup(bmg, peerplays_instance=ctx.peerplays)
    click.echo(pretty_print(bmg.bettingmarkets, ctx=ctx))


@bookie.command()
@click.pass_context
@onlineChain
def rules(ctx):
    """ [bookie] List all rules
    """
    rules = Rules(peerplays_instance=ctx.peerplays)
    click.echo(pretty_print(rules, ctx=ctx))


@bookie.command()
@click.argument("rule")
@click.pass_context
@onlineChain
def rule(ctx, rule):
    """ [bookie] Show a specific rule

        :param str bmg: Betting market id
    """
    rule = Rule(rule, peerplays_instance=ctx.peerplays)
    t = PrettyTable([
        "id",
        "name",
    ])
    t.align = "l"
    t.add_row([
        rule["id"],
        "\n".join(["{}: {}".format(v[0], v[1]) for v in rule["name"]]),
    ])
    click.echo(str(t))
    click.echo(
        "\n".join(["{}: {}".format(v[0], v[1]) for v in rule["description"]])
    )


@bookie.command()
@click.argument("sport", default=None, required=False)
@click.pass_context
@onlineChain
def list(ctx, sport):
    """ [bookie] list the entire thing
    """
    from .ui import maplist2dict
    from tqdm import tqdm
    from treelib import Node, Tree
    tree = Tree()
    tree.create_node("sports", "root")

    def formatname(o):
        if "name" in o:
            name = o.get("name")
        elif "description" in o:
            name = o.get("description")
        else:
            name = []
        return "{} ({})".format(
            maplist2dict(name).get("en"),
            o["id"]
        )

    if sport:
        sports = [Sport(sport, peerplays_instance=ctx.peerplays)]
    else:
        sports = Sports()

    for sport in tqdm(sports):
        tree.create_node(
            formatname(sport),
            sport["id"],
            parent="root")

        for eg in tqdm(sport.eventgroups):
            tree.create_node(
                formatname(eg),
                eg["id"],
                parent=sport["id"])

            for e in tqdm(eg.events):
                tree.create_node(
                    formatname(e),
                    e["id"],
                    parent=eg["id"])

                for bmg in tqdm(e.bettingmarketgroups):
                    tree.create_node(
                        formatname(bmg),
                        bmg["id"],
                        parent=e["id"])

                    for bm in tqdm(bmg.bettingmarkets):
                        tree.create_node(
                            formatname(bm),
                            bm["id"],
                            parent=bmg["id"])

    tree.show()
