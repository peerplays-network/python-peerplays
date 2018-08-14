from .decorators import (
    onlineChain,
)

import click

from peerplays.asset import Asset
from peerplays.exceptions import AssetDoesNotExistsException

from prettytable import PrettyTable

from .main import main


@main.command()
@click.pass_context
@onlineChain
def assets(ctx):
    "List Assets"
    MAX_ASSET = 100000
    assets = []
    for i in range(0, MAX_ASSET):
        try: 
            assets.append(Asset("1.3.{}".format(i)))
        except AssetDoesNotExistsException:
            break
    
    assetTable = PrettyTable()
    assetTable.field_names = ["ID", "Symbol", "Precision", "Description", "Max Supply"]

    for i in range (0, len(assets)):
        try: 
            description = assets[i].description
            if description == "":
                description = "--"
        except AttributeError:
            description = "--"
        assetTable.add_row([assets[i].id, assets[i].symbol, assets[i].precision, description, assets[i].max_supply["amount"]])

    click.echo(assetTable)