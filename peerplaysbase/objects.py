import json
from collections import OrderedDict
from graphenebase.types import (
    Uint8, Int16, Uint16, Uint32, Uint64,
    Varint32, Int64, String, Bytes, Void,
    Array, PointInTime, Signature, Bool,
    Set, Fixed_array, Optional, Static_variant,
    Map, Id, VoteId,
    ObjectId as GPHObjectId,
)
from graphenebase.objects import GrapheneObject, isArgsThisClass
from .chains import known_chains
from .objecttypes import object_type
from .account import PublicKey
from graphenebase.objects import Operation as GPHOperation
from .operationids import operations
from .types import Enum
default_prefix = "PPY"


class ObjectId(GPHObjectId):
    """ Encodes object/protocol ids
    """
    # Overloading to get local obect_type
    def __init__(self, object_str, type_verify=None):
        if len(object_str.split(".")) == 3:
            space, type, id = object_str.split(".")
            self.space = int(space)
            self.type = int(type)
            self.instance = Id(int(id))
            self.Id = object_str
            if type_verify:
                assert object_type[type_verify] == int(type),\
                    "Object id does not match object type! " +\
                    "Excpected %d, got %d" %\
                    (object_type[type_verify], int(type))
        else:
            raise Exception("Object id is invalid")


class Operation(GPHOperation):
    def __init__(self, *args, **kwargs):
        super(Operation, self).__init__(*args, **kwargs)

    def _getklass(self, name):
        module = __import__("peerplaysbase.operations", fromlist=["operations"])
        class_ = getattr(module, name)
        return class_

    def operations(self):
        return operations

    def getOperationNameForId(self, i):
        """ Convert an operation id into the corresponding string
        """
        for key in operations:
            if int(operations[key]) is int(i):
                return key
        return "Unknown Operation ID %d" % i

    def json(self):
        return json.loads(str(self))


class Asset(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('amount', Int64(kwargs["amount"])),
                ('asset_id', ObjectId(kwargs["asset_id"], "asset"))
            ]))


class Memo(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "message" in kwargs and kwargs["message"]:
                prefix = kwargs.pop("prefix", default_prefix)
                super().__init__(OrderedDict([
                    ('from', PublicKey(kwargs["from"], prefix=prefix)),
                    ('to', PublicKey(kwargs["to"], prefix=prefix)),
                    ('nonce', Uint64(int(kwargs["nonce"]))),
                    ('message', Bytes(kwargs["message"]))
                ]))
            else:
                super().__init__(None)


class Price(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('base', Asset(kwargs["base"])),
                ('quote', Asset(kwargs["quote"]))
            ]))


class Permission(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            prefix = kwargs.pop("prefix", default_prefix)

            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            # Sort keys (FIXME: ideally, the sorting is part of Public
            # Key and not located here)
            kwargs["key_auths"] = sorted(
                kwargs["key_auths"],
                key=lambda x: repr(PublicKey(x[0], prefix=prefix).address),
                reverse=False,
            )
            accountAuths = Map([
                [ObjectId(e[0], "account"), Uint16(e[1])]
                for e in kwargs["account_auths"]
            ])
            keyAuths = Map([
                [PublicKey(e[0], prefix=prefix), Uint16(e[1])]
                for e in kwargs["key_auths"]
            ])
            super().__init__(OrderedDict([
                ('weight_threshold', Uint32(int(kwargs["weight_threshold"]))),
                ('account_auths', accountAuths),
                ('key_auths', keyAuths),
                ('extensions', Set([])),
            ]))


class AccountOptions(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        prefix = kwargs.pop("prefix", default_prefix)

        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            # remove dublicates
            kwargs["votes"] = list(set(kwargs["votes"]))
            # Sort votes
            kwargs["votes"] = sorted(
                kwargs["votes"],
                key=lambda x: float(x.split(":")[1]),
            )
            super().__init__(OrderedDict([
                ('memo_key', PublicKey(kwargs["memo_key"], prefix=prefix)),
                ('voting_account', ObjectId(kwargs["voting_account"], "account")),
                ('num_witness', Uint16(kwargs["num_witness"])),
                ('num_committee', Uint16(kwargs["num_committee"])),
                ('votes', Array([VoteId(o) for o in kwargs["votes"]])),
                ('extensions', Set([])),
            ]))


class BetType(Enum):
    options = [
        "back",
        "lay",
    ]


class BettingMarketResolution(Enum):
    options = [
        "win",
        "not_win",
        "cancel",
        "BETTING_MARKET_RESOLUTION_COUNT",
    ]


class AssetOptions(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('max_supply', Int64(kwargs["max_supply"])),
                ('market_fee_percent', Uint16(kwargs["market_fee_percent"])),
                ('max_market_fee', Int64(kwargs["max_market_fee"])),
                ('issuer_permissions', Uint16(kwargs["issuer_permissions"])),
                ('flags', Uint16(kwargs["flags"])),
                ('core_exchange_rate', Price(kwargs["core_exchange_rate"])),
                ('whitelist_authorities',
                    Array([ObjectId(x, "account") for x in kwargs["whitelist_authorities"]])),
                ('blacklist_authorities',
                    Array([ObjectId(x, "account") for x in kwargs["blacklist_authorities"]])),
                ('whitelist_markets',
                    Array([ObjectId(x, "asset") for x in kwargs["whitelist_markets"]])),
                ('blacklist_markets',
                    Array([ObjectId(x, "asset") for x in kwargs["blacklist_markets"]])),
                ('description', String(kwargs["description"])),
                ('extensions', Set([])),
            ]))


class BitAssetOptions(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('feed_lifetime_sec', Uint32(kwargs["feed_lifetime_sec"])),
                ('minimum_feeds', Uint8(kwargs["minimum_feeds"])),
                ('force_settlement_delay_sec', Uint32(kwargs["force_settlement_delay_sec"])),
                ('force_settlement_offset_percent', Uint16(kwargs["force_settlement_offset_percent"])),
                ('maximum_force_settlement_volume', Uint16(kwargs["maximum_force_settlement_volume"])),
                ('short_backing_asset', ObjectId(kwargs["short_backing_asset"], "asset")),
                ('extensions', Set([])),
            ]))


class DividendAssetOptions(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            if "next_payout_time" in kwargs:
                next_payout_time = Optional(PointInTime(kwargs["next_payout_time"]))
            else:
                next_payout_time = Optional(None)

            if "payout_interval" in kwargs:
                payout_interval = Optional(Uint32(kwargs["payout_interval"]))
            else:
                payout_interval = Optional(None)

            super().__init__(OrderedDict([
                ('next_payout_time', next_payout_time),
                ('payout_interval', payout_interval),
                ('minimum_fee_percentage', Uint64(kwargs["minimum_fee_percentage"])),
                ('minimum_distribution_interval', Uint32(kwargs["minimum_distribution_interval"])),
                ('extensions', Set([])),
            ]))
