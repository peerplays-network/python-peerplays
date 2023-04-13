import json
from peerplays.account import Account
from peerplays.amount import Amount
from prettytable import PrettyTable, ALL as allBorders
import pkg_resources
import click
import logging
log = logging.getLogger(__name__)


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('{prog} {version}'.format(
        prog=pkg_resources.require("peerplays")[0].project_name,
        version=pkg_resources.require("peerplays")[0].version
    ))
    ctx.exit()


def print_permissions(account):
    t = PrettyTable(
        ["Permission", "Threshold", "Key/Account"],
        hrules=allBorders
    )
    t.align = "r"
    for permission in ["owner", "active"]:
        auths = []
        # account auths:
        for authority in account[permission]["account_auths"]:
            auths.append(
                "%s (%d)" % (Account(authority[0])["name"],
                             authority[1]))
        # key auths:
        for authority in account[permission]["key_auths"]:
            auths.append(
                "%s (%d)" % (authority[0], authority[1]))
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


def pprintOperation(op, show_memo=False, ctx=None):
    from peerplays.price import Order, FilledOrder

    if isinstance(op, dict) and "op" in op:
        id = op["op"][0]
        results = op["result"]
        op = op["op"][1]
    else:
        id = op[0]
        op = op[1]
        results = []
    if id == 1:
        return str(Order(op))
    elif id == 4:
        return str(FilledOrder(op))
    elif id == 5:
        return "New account created for {}".format(op["name"])
    elif id == 2:
        return "Canceled order %s" % op["order"]
    elif id == 6:
        return "Account {} updated".format(Account(op["account"])["name"])
    elif id == 8:
        account_to_upgrade = Account(op["account_to_upgrade"])["name"]
        return "Account {} upgraded to Lifetime Membership for {}".format(
            account_to_upgrade, Amount(op["fee"])
        ) if op["upgrade_to_lifetime_member"] else "Account {} upgraded".format(
            account_to_upgrade
        )
    elif id == 32:
        return "Account %s vested %s for %s as type %s" % (
            Account(op["creator"])["name"],
            Amount(op["amount"]),
            Account(op["owner"])["name"],
            op["balance_type"]
        )
    elif id == 33:
        return "Claiming from vesting: %s" % str(Amount(op["amount"]))
    elif id == 37:
        claimant_account = Account(op["deposit_to_account"])
        amount = Amount(op["total_claimed"])
        return "Claiming {amount} for {claimant_account[name]}".format(**locals())
    elif id == 10:
        return "Create asset %s" % op["symbol"]
    elif id == 14:
        from_account = Account(op["issuer"])["name"]
        to_account = Account(op["issue_to_account"])["name"]
        amount = Amount(op["asset_to_issue"])
        return "Issuer {from_account} issued {amount} to {to_account}".format(
            **locals()
        )
    elif id == 15:
        return "Reserve {}".format(str(Amount(op["amount_to_reserve"])))
    elif id == 0:
        from_account = Account(op["from"])
        to_account = Account(op["to"])
        amount = Amount(op["amount"])
        memo = ""
        if show_memo and ctx is not None:
            try:
                plain_memo = Memo(blockchain_instance=ctx.blockchain).decrypt(
                    op["memo"]
                )
            except Exception as e:
                plain_memo = str(e)
            memo = " (memo: {plain_memo})".format(**locals())
        return "Transfer from {from_account[name]} to {to_account[name]}: {amount}{memo}".format(
            **locals()
        )
    elif id == 88:
        return "Offer to %s NFTs %s" % (
            "BUY" if op["buying_item"] else "SELL", op["item_ids"]
        )
    elif id == 89:
        return "Account {} bid {} against offer {}".format(
            Account(op["bidder"])["name"], Amount(op["bid_price"]), op["offer_id"]
        )
    elif id == 91:
        return "Offer %s %s" % (op["offer_id"], op["result"])
    elif id == 92:
        return "Create NFT series %s (%s)"%(op["name"], op["symbol"])
    elif id == 93:
        return "Update NFT series %s"%(op["nft_metadata_id"])
    elif id == 94:
        from_account = Account(op["payer"])["name"]
        to_account = Account(op["owner"])["name"]
        nft_series = op["nft_metadata_id"]
        return "Account {from_account} minted an NFT in series {nft_series} to {to_account}".format(
            **locals()
        )
    elif id == 101:
        return "Created SON"
    elif id == 102:
        return "Updated SON"
    elif id == 104:
        return "SON Heartbeat"
    else:
        return json.dumps(op, indent=4)


def pretty_print(o, *args, **kwargs):
    t = PrettyTable(
        o[0].keys(),
    )
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


def maplist2dict(dlist):
    """ Convert a list of tuples into a dictionary
    """
    return {k[0]: k[1] for k in dlist}
