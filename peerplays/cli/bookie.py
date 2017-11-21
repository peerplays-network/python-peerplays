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


@bookie.command()
@click.pass_context
@onlineChain
def sports(ctx):
    """ [bookie] List sports """
    sports = Sports(peerplays_instance=ctx.peerplays)
    t = PrettyTable(["id", "name"])
    t.align = "l"
    for sport in sports:
        t.add_row([
            sport["id"],
            "\n".join(["{}: {}".format(v[0], v[1]) for v in sport["name"]])
        ])
    click.echo(str(t))


@bookie.command()
@click.argument("sport")
@click.pass_context
@onlineChain
def eventgroups(ctx, sport):
    """ [bookie] List event groups for a sport

        :param str sport: Sports id
    """
    sport = Sport(sport, peerplays_instance=ctx.peerplays)
    t = PrettyTable(["id", "name"])
    t.align = "l"
    for eg in sport.eventgroups:
        t.add_row([
            eg["id"],
            "\n".join(["{}: {}".format(v[0], v[1]) for v in eg["name"]])
        ])
    click.echo(str(t))


@bookie.command()
@click.argument("eventgroup")
@click.pass_context
@onlineChain
def events(ctx, eventgroup):
    """ [bookie] List events for an event group

        :param str eventgroup: Event Group id
    """
    eg = EventGroup(eventgroup, peerplays_instance=ctx.peerplays)
    t = PrettyTable([
        "id",
        "name",
        "season",
        "start_time",
        "status",
    ])
    t.align = "l"
    for event in eg.events:
        t.add_row([
            event["id"],
            "\n".join(["{}: {}".format(v[0], v[1]) for v in event["name"]]),
            "\n".join(["{}: {}".format(v[0], v[1]) for v in event["season"]]),
            event["start_time"],
            event["status"],
        ])
    click.echo(str(t))


@bookie.command()
@click.argument("event")
@click.pass_context
@onlineChain
def bmgs(ctx, event):
    """ [bookie] List betting market groups for an event

        :param str event: Event id
    """
    eg = Event(event, peerplays_instance=ctx.peerplays)
    t = PrettyTable([
        "id",
        "description",
        "event_id",
        "rules_id",
        "matched_amount",
    ])
    t.align = "l"
    for bmg in eg.bettingmarketgroups:
        asset = Asset(bmg["asset_id"])
        t.add_row([
            bmg["id"],
            "\n".join(["{}: {}".format(v[0], v[1]) for v in bmg["description"]]),
            bmg["event_id"],
            bmg["rules_id"],
            "{} {}".format(
                bmg["total_matched_bets_amount"] / 10 ** asset["precision"],
                asset["symbol"]
            ),
        ])
    click.echo(str(t))


@bookie.command()
@click.argument("bmg")
@click.pass_context
@onlineChain
def bettingmarkets(ctx, bmg):
    """ [bookie] List betting markets for bmg

        :param str bmg: Betting market id
    """
    bmg = BettingMarketGroup(bmg, peerplays_instance=ctx.peerplays)
    t = PrettyTable([
        "id",
        "description",
        "group_id",
    ])
    t.align = "l"
    for market in bmg.bettingmarkets:
        asset = Asset(bmg["asset_id"])
        t.add_row([
            market["id"],
            "\n".join(["{}: {}".format(v[0], v[1]) for v in market["description"]]),
            market["group_id"],
        ])
    click.echo(str(t))


@bookie.command()
@click.pass_context
@onlineChain
def rules(ctx):
    """ [bookie] List all rules
    """
    rules = Rules(peerplays_instance=ctx.peerplays)
    t = PrettyTable([
        "id",
        "name",
    ])
    t.align = "l"
    for rule in rules:
        t.add_row([
            rule["id"],
            "\n".join(["{}: {}".format(v[0], v[1]) for v in rule["name"]]),
        ])
    click.echo(str(t))


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
