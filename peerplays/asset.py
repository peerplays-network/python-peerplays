import json
from peerplaysbase.asset_permissions import todict
from .blockchainobject import BlockchainObject
from .exceptions import AssetDoesNotExistsException
from .instance import BlockchainInstance

from graphenecommon.asset import Asset as GrapheneAsset


@BlockchainInstance.inject
class Asset(GrapheneAsset):
    """ Deals with Assets of the network.

        :param str Asset: Symbol name or object id of an asset
        :param bool lazy: Lazy loading
        :param bool full: Also obtain bitasset-data and dynamic asset data
        :param bitshares.bitshares.BitShares blockchain_instance: BitShares
            instance
        :returns: All data of an asset
        :rtype: dict

        .. note:: This class comes with its own caching function to reduce the
                  load on the API server. Instances of this class can be
                  refreshed with ``Asset.refresh()``.
    """

    def define_classes(self):
        self.type_id = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Permissions and flags
        self["permissions"] = todict(self["options"].get("issuer_permissions"))
        self["flags"] = todict(self["options"].get("flags"))
        try:
            self["description"] = json.loads(self["options"]["description"])
        except Exception:
            self["description"] = self["options"]["description"]
