import json
from peerplaysbase.asset_permissions import todict
from .exceptions import AssetDoesNotExistsException
from .blockchainobject import BlockchainObject


class Asset(BlockchainObject):
    """ Deals with Assets of the network.

        :param str Asset: Symbol name or object id of an asset
        :param bool lazy: Lazy loading
        :param bool full: Also obtain bitasset-data and dynamic asset data
        :param peerplays.peerplays.PeerPlays blockchain_instance: PeerPlays
            instance
        :returns: All data of an asset
        :rtype: dict

        .. note:: This class comes with its own caching function to reduce the
                  load on the API server. Instances of this class can be
                  refreshed with ``Asset.refresh()``.
    """
    type_id = 3

    def __init__(self, *args, **kwargs):
        self.full = kwargs.pop("full", False)
        super().__init__(*args, **kwargs)

    def refresh(self):
        """ Refresh the data from the API server
        """
        asset = self.blockchain.rpc.get_asset(self.identifier)
        if not asset:
            raise AssetDoesNotExistsException(self.identifier)
        super(Asset, self).__init__(asset, blockchain_instance=self.blockchain)
        if self.full:
            if "bitasset_data_id" in asset:
                self["bitasset_data"] = self.blockchain.rpc.get_object(
                    asset["bitasset_data_id"])
            self["dynamic_asset_data"] = self.blockchain.rpc.get_object(
                asset["dynamic_asset_data_id"])

        # Permissions and flags
        self["permissions"] = todict(asset["options"].get(
            "issuer_permissions"))
        self["flags"] = todict(asset["options"].get("flags"))
        self["max_supply"] = asset["options"].get("max_supply")
        try:
            self["description"] = json.loads(asset["options"]["description"])
        except:
            self["description"] = asset["options"]["description"]

    @property
    def is_fully_loaded(self):
        """ Is this instance fully loaded / e.g. all data available?
        """
        return (
            self.full and
            "bitasset_data_id" in self and
            "bitasset_data" in self
        )

    @property
    def id(self):
        return self['id']

    @property
    def symbol(self):
        return self["symbol"]

    @property
    def description(self):
        return self["description"]

    @property
    def precision(self):
        return self["precision"]

    @property
    def max_supply(self):
        from .amount import Amount
        return Amount({
            "amount": self["max_supply"],
            "asset_id": self["id"]
        })

    @property
    def is_bitasset(self):
        """ Is the asset a :doc:`mpa`?
        """
        return ("bitasset_data_id" in self)

    @property
    def permissions(self):
        """ List the permissions for this asset that the issuer can obtain
        """
        return self["permissions"]

    @property
    def flags(self):
        """ List the permissions that are currently used (flags)
        """
        return self["flags"]

    def ensure_full(self):
        if not self.is_fully_loaded:
            self.full = True
            self.refresh()
