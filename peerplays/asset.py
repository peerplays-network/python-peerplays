import json
from .exceptions import AssetDoesNotExistsException
from .blockchainobject import BlockchainObject


class Asset(BlockchainObject):
    """ Deals with Assets of the network.

        :param str Asset: Symbol name or object id of an asset
        :param bool lazy: Lazy loading
        :param bool full: Also obtain bitasset-data and dynamic asset dat
        :param peerplays.peerplays.PeerPlays peerplays_instance: PeerPlays instance
        :returns: All data of an asset
        :rtype: dict

        .. note:: This class comes with its own caching function to reduce the
                  load on the API server. Instances of this class can be
                  refreshed with ``Asset.refresh()``.
    """
    type_id = 3

    def __init__(
        self,
        asset,
        lazy=False,
        full=False,
        peerplays_instance=None
    ):
        self.full = full
        super().__init__(
            asset,
            lazy=lazy,
            full=full,
            peerplays_instance=peerplays_instance,
        )

    def refresh(self):
        """ Refresh the data from the API server
        """
        from peerplaysbase import asset_permissions

        asset = self.peerplays.rpc.get_asset(self.identifier)
        if not asset:
            raise AssetDoesNotExistsException
        super(Asset, self).__init__(asset)
        if self.full:
            if self.is_bitasset:
                self["bitasset_data"] = self.peerplays.rpc.get_object(asset["bitasset_data_id"])
            self["dynamic_asset_data"] = self.peerplays.rpc.get_object(asset["dynamic_asset_data_id"])

        # Permissions and flags
        self["permissions"] = asset_permissions.todict(asset["options"]["issuer_permissions"])
        self["flags"] = asset_permissions.todict(asset["options"]["flags"])
        try:
            self["description"] = json.loads(asset["options"]["description"])
        except:
            self["description"] = asset["options"]["description"]

    @property
    def symbol(self):
        return self["symbol"]

    @property
    def precision(self):
        return self["precision"]

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
        if not self.full:
            self.full = True
            self.refresh()
