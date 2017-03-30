import json
import sys
from peerplays import PeerPlays
from peerplays.account import Account
from peerplays.instance import set_shared_peerplays_instance
from prettytable import PrettyTable, ALL as allBorders
from functools import update_wrapper
import pkg_resources
import click
import logging
log = logging.getLogger(__name__)


def verbose(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        global log
        verbosity = [
            "critical", "error", "warn", "info", "debug"
        ][int(min(ctx.obj.get("verbose", 0), 4))]
        log.setLevel(getattr(logging, verbosity.upper()))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, verbosity.upper()))
        ch.setFormatter(formatter)
        log.addHandler(ch)

        # GrapheneAPI logging
        if ctx.obj["verbose"] > 4:
            verbosity = [
                "critical", "error", "warn", "info", "debug"
            ][int(min(ctx.obj.get("verbose", 4) - 4, 4))]
            log = logging.getLogger("grapheneapi")
            log.setLevel(getattr(logging, verbosity.upper()))
            log.addHandler(ch)

        if ctx.obj["verbose"] > 8:
            verbosity = [
                "critical", "error", "warn", "info", "debug"
            ][int(min(ctx.obj.get("verbose", 8) - 8, 4))]
            log = logging.getLogger("graphenebase")
            log.setLevel(getattr(logging, verbosity.upper()))
            log.addHandler(ch)

        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def offlineChain(f):
    @click.pass_context
    @verbose
    def new_func(ctx, *args, **kwargs):
        ctx.obj["offline"] = True
        ctx.peerplays = PeerPlays(**ctx.obj)
        set_shared_peerplays_instance(ctx.peerplays)
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def onlineChain(f):
    @click.pass_context
    @verbose
    def new_func(ctx, *args, **kwargs):
        ctx.peerplays = PeerPlays(**ctx.obj)
        set_shared_peerplays_instance(ctx.peerplays)
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def unlockWallet(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        if not ctx.obj.get("unsigned", False):
            if ctx.peerplays.wallet.created():
                pwd = click.prompt("Current Wallet Passphrase", hide_input=True)
                ctx.peerplays.wallet.unlock(pwd)
            else:
                click.echo("No wallet installed yet. Creating ...")
                pwd = click.prompt("Wallet Encryption Passphrase", hide_input=True, confirmation_prompt=True)
                ctx.peerplays.wallet.create(pwd)
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('{prog} {version}'.format(
        prog=pkg_resources.require("uptick")[0].project_name,
        version=pkg_resources.require("uptick")[0].version
    ))
    ctx.exit()


def print_permissions(account):
    t = PrettyTable(["Permission", "Threshold", "Key/Account"], hrules=allBorders)
    t.align = "r"
    for permission in ["owner", "active"]:
        auths = []
        # account auths:
        for authority in account[permission]["account_auths"]:
            auths.append("%s (%d)" % (Account(authority[0])["name"], authority[1]))
        # key auths:
        for authority in account[permission]["key_auths"]:
            auths.append("%s (%d)" % (authority[0], authority[1]))
        t.add_row([
            permission,
            account[permission]["weight_threshold"],
            "\n".join(auths),
        ])
    print(t)


def get_terminal(text="Password", confirm=False, allowedempty=False):
    import getpass
    while True:
        pw = getpass.getpass(text)
        if not pw and not allowedempty:
            print("Cannot be empty!")
            continue
        else:
            if not confirm:
                break
            pwck = getpass.getpass(
                "Confirm " + text
            )
            if (pw == pwck):
                break
            else:
                print("Not matching!")
    return pw


def pprintOperation(op):
    return json.dumps(op["op"][1], indent=4)
