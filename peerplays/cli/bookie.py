import click
from pprint import pprint
from prettytable import PrettyTable
from .decorators import onlineChain
from .main import main

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


def pretty_print(o):
    t = PrettyTable(o[0].keys())
    for items in o:
        r = list()
        for item in items.values():
            if isinstance(item, list):
                r.append(
                    "\n".join(["{}: {}".format(v[0], v[1]) for v in item])
                )
            else:
                r.append(item)
        t.add_row(r)
    t.align = "l"
    return str(t)


@bookie.command()
@click.pass_context
@onlineChain
def sports(ctx):
    """ [bookie] List sports """
    sports = Sports(peerplays_instance=ctx.peerplays)
    click.echo(pretty_print(sports))


@bookie.command()
@click.argument("sport")
@click.pass_context
@onlineChain
def eventgroups(ctx, sport):
    """ [bookie] List event groups for a sport

        :param str sport: Sports id
    """
    sport = Sport(sport, peerplays_instance=ctx.peerplays)
    click.echo(pretty_print(sport.eventgroups))


@bookie.command()
@click.argument("eventgroup")
@click.pass_context
@onlineChain
def events(ctx, eventgroup):
    """ [bookie] List events for an event group

        :param str eventgroup: Event Group id
    """
    eg = EventGroup(eventgroup, peerplays_instance=ctx.peerplays)
    click.echo(pretty_print(eg.events))


@bookie.command()
@click.argument("event")
@click.pass_context
@onlineChain
def bmgs(ctx, event):
    """ [bookie] List betting market groups for an event

        :param str event: Event id
    """
    eg = Event(event, peerplays_instance=ctx.peerplays)
    click.echo(pretty_print(eg.bettingmarketgroups))


@bookie.command()
@click.argument("bmg")
@click.pass_context
@onlineChain
def bettingmarkets(ctx, bmg):
    """ [bookie] List betting markets for bmg

        :param str bmg: Betting market id
    """
    bmg = BettingMarketGroup(bmg, peerplays_instance=ctx.peerplays)
    click.echo(pretty_print(bmg.bettingmarkets))


@bookie.command()
@click.pass_context
@onlineChain
def rules(ctx):
    """ [bookie] List all rules
    """
    rules = Rules(peerplays_instance=ctx.peerplays)
    click.echo(pretty_print(rules))


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
