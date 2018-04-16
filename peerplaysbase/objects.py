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
from .types import Enum, Sha256
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


class BettingMarketStatus(Enum):
    options = [
        "unresolved",  # no grading  has been published for this betting market
        "frozen",      # bets are suspended, no bets allowed
        "graded",      # grading of win or not_win has been published
        "canceled",    # the betting market is canceled, no further bets are allowed
        "settled",     # the betting market has been paid out
        "BETTING_MARKET_STATUS_COUNT"
    ]


class BettingMarketGroupStatus(Enum):
    options = [
        "upcoming",    # betting markets are accepting bets, will never go "in_play"
        "in_play",     # betting markets are delaying bets
        "closed",      # betting markets are no longer accepting bets
        "graded",      # witnesses have published win/not win for the betting markets
        "re_grading",  # initial win/not win grading has been challenged
        "settled",     # paid out
        "frozen",      # betting markets are not accepting bets
        "canceled",    # canceled
        "BETTING_MARKET_GROUP_STATUS_COUNT"
    ]


class EventStatus(Enum):
    options = [
        "upcoming",     # Event has not started yet, betting is allowed
        "in_progress",  # Event is in progress, if "in-play" betting is enabled, bets will be delayed
        "frozen",       # Betting is temporarily disabled
        "finished",     # Event has finished, no more betting allowed
        "canceled",     # Event has been canceled, all betting markets have been canceled
        "settled",      # All betting markets have been paid out
        "STATUS_COUNT"
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


class Rock_paper_scissors_gesture(Enum):
    options = [
        "rock",
        "paper",
        "scissors",
        "spock",
        "lizard"
    ]


class GameSpecificMoves(Static_variant):
    def __init__(self, o):

        class rock_paper_scissors_throw_commit(GrapheneObject):
            def __init__(self, *args, **kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('nonce1',
                         Uint64(kwargs["nonce1"])),
                        ('throw_hash',
                         Sha256(kwargs["throw_hash"])),
                    ]))

        class rock_paper_scissors_throw_reveal(GrapheneObject):
            def __init__(self, *args, **kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('nonce2',
                         Uint64(kwargs["nonce2"])),
                        ('gesture',
                         Rock_paper_scissors_gesture(kwargs["gesture"])),
                    ]))

        id = o[0]
        if id == 0:
            data = rock_paper_scissors_throw_commit(o[1])
        elif id == 1:
            data = rock_paper_scissors_throw_reveal(o[1])
        else:
            raise Exception(
                "Unknown game-specific move: {}".format(id))
        super().__init__(data, id)


class GameSpecificOptions(Static_variant):
    def __init__(self, o):

        class rock_paper_scissors_game_options(GrapheneObject):
            def __init__(self, *args, **kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('insurance_enabled',
                         Bool(kwargs["insurance_enabled"])),
                        ('time_per_commit_move',
                         Uint32(kwargs["time_per_commit_move"])),
                        ('time_per_reveal_move',
                         Uint32(kwargs["time_per_reveal_move"])),
                        ('number_of_gestures',
                         Uint8(kwargs["number_of_gestures"])),
                    ]))

        id = o[0]
        if id == 0:
            data = rock_paper_scissors_game_options(o[1])
        else:
            raise Exception("Unknown game-specific options")
        super().__init__(data, id)


class TournamentOptions(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            start_time = Optional(PointInTime(kwargs["start_time"])
                                  if "start_time" in kwargs else
                                  None)
            start_delay = Optional(Uint32(kwargs["start_delay"])
                                   if "start_delay" in kwargs else
                                   None)

            if "meta" in kwargs and kwargs["meta"]:
                raise NotImplementedError('"meta" cannot yet be used with this library')

            super().__init__(OrderedDict([
                ('registration_deadline',
                 PointInTime(kwargs["registration_deadline"])),
                ('number_of_players',
                 Uint32(kwargs["number_of_players"])),
                ('buy_in', Asset(kwargs["buy_in"])),
                ('whitelist',
                    Array([ObjectId(x, "account")
                           for x in kwargs["whitelist"]])),
                ('start_time', start_time),
                ('start_delay', start_delay),
                ('round_delay', Uint32(kwargs["round_delay"])),
                ('number_of_wins', Uint32(kwargs["number_of_wins"])),
                ('meta', Optional(None)),
                ('game_options', GameSpecificOptions(kwargs["game_options"])),
            ]))
