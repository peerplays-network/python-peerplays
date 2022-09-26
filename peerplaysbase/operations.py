from collections import OrderedDict
from graphenebase.types import (
    Uint8,
    Int16,
    Uint16,
    Uint32,
    Uint64,
    Varint32,
    Int64,
    String,
    Bytes,
    Void,
    Array,
    PointInTime,
    Signature,
    Bool,
    Set,
    Fixed_array,
    Optional,
    Static_variant,
    Map,
    Id,
    VoteId,
    FullObjectId,
)
from .objects import GrapheneObject, isArgsThisClass
from .account import PublicKey
from .operationids import operations, getOperationNameForId
from .objects import (
    Operation,
    Asset,
    Price,
    Permission,
    AccountOptions,
    Memo,
    ObjectId,
    AssetOptions,
    BitAssetOptions,
    BetType,
    EventStatus,
    BettingMarketResolution,
    BettingMarketStatus,
    BettingMarketGroupStatus,
    TournamentOptions,
    GameSpecificMoves,
    ResolutionConstraint,
)
from .types import Double

default_prefix = "PPY"


class Transfer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            prefix = kwargs.get("prefix", default_prefix)

            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" in kwargs and kwargs["memo"]:
                memo = Optional(Memo(prefix=prefix, **kwargs["memo"]))
            else:
                memo = Optional(None)
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("from", ObjectId(kwargs["from"], "account")),
                        ("to", ObjectId(kwargs["to"], "account")),
                        ("amount", Asset(kwargs["amount"])),
                        ("memo", memo),
                        ("extensions", Set([])),
                    ]
                )
            )

class Limit_order_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("seller", ObjectId(kwargs["seller"], "account")),
                        ("amount_to_sell", Asset(kwargs["amount_to_sell"])),
                        ("min_to_receive", Asset(kwargs["min_to_receive"])),
                        ("expiration", PointInTime(kwargs["expiration"])),
                        ("fill_or_kill", Bool(kwargs["fill_or_kill"])),
                        ("extensions", Set([])),
                    ]
                )
            )

class Limit_order_cancel(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        (
                            "fee_paying_account",
                            ObjectId(kwargs["fee_paying_account"], "account"),
                        ),
                        ("order", ObjectId(kwargs["order"], "limit_order")),
                        ("extensions", Set([])),
                    ]
                )
            )

class Account_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("registrar", ObjectId(kwargs["registrar"], "account")),
                        ("referrer", ObjectId(kwargs["referrer"], "account")),
                        ("referrer_percent", Uint16(kwargs["referrer_percent"])),
                        ("name", String(kwargs["name"])),
                        ("owner", Permission(kwargs["owner"], prefix=prefix)),
                        ("active", Permission(kwargs["active"], prefix=prefix)),
                        ("options", AccountOptions(kwargs["options"], prefix=prefix)),
                        ("extensions", Set([])),
                    ]
                )
            )


class Account_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)
            if "owner" in kwargs:
                owner = Optional(Permission(kwargs["owner"], prefix=prefix))
            else:
                owner = Optional(None)
            if "active" in kwargs:
                active = Optional(Permission(kwargs["active"], prefix=prefix))
            else:
                active = Optional(None)
            if "new_options" in kwargs:
                options = Optional(AccountOptions(kwargs["new_options"], prefix=prefix))
            else:
                options = Optional(None)
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("account", ObjectId(kwargs["account"], "account")),
                        ("owner", owner),
                        ("active", active),
                        ("new_options", options),
                        ("extensions", Set([])),
                    ]
                )
            )


class Account_upgrade(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        (
                            "account_to_upgrade",
                            ObjectId(kwargs["account_to_upgrade"], "account"),
                        ),
                        (
                            "upgrade_to_lifetime_member",
                            Bool(kwargs["upgrade_to_lifetime_member"]),
                        ),
                        ("extensions", Set([])),
                    ]
                )
            )


class Asset_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "bitasset_opts" in kwargs:
                bitasset_opts = Optional(BitAssetOptions(kwargs["bitasset_opts"]))
            else:
                bitasset_opts = Optional(None)
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("issuer", ObjectId(kwargs["issuer"], "account")),
                        ("symbol", String(kwargs["symbol"])),
                        ("precision", Uint8(kwargs["precision"])),
                        ("common_options", AssetOptions(kwargs["common_options"])),
                        ("bitasset_opts", bitasset_opts),
                        (
                            "is_prediction_market",
                            Bool(bool(kwargs["is_prediction_market"])),
                        ),
                        ("extensions", Set([])),
                    ]
                )
            )


class Asset_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "new_issuer" in kwargs:
                new_issuer = Optional(ObjectId(kwargs["new_issuer"], "account"))
            else:
                new_issuer = Optional(None)
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("issuer", ObjectId(kwargs["issuer"], "account")),
                        (
                            "asset_to_update",
                            ObjectId(kwargs["asset_to_update"], "asset"),
                        ),
                        ("new_issuer", new_issuer),
                        ("new_options", AssetOptions(kwargs["new_options"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Asset_update_bitasset(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("issuer", ObjectId(kwargs["issuer"], "account")),
                        (
                            "asset_to_update",
                            ObjectId(kwargs["asset_to_update"], "asset"),
                        ),
                        ("new_options", BitAssetOptions(kwargs["new_options"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Asset_issue(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            prefix = kwargs.get("prefix", default_prefix)

            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" in kwargs and kwargs["memo"]:
                memo = Optional(Memo(prefix=prefix, **kwargs["memo"]))
            else:
                memo = Optional(None)
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("issuer", ObjectId(kwargs["issuer"], "account")),
                        ("asset_to_issue", Asset(kwargs["asset_to_issue"])),
                        (
                            "issue_to_account",
                            ObjectId(kwargs["issue_to_account"], "account"),
                        ),
                        ("memo", memo),
                        ("extensions", Set([])),
                    ]
                )
            )


class Op_wrapper(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([("op", Operation(kwargs["op"]))]))


class Proposal_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "review_period_seconds" in kwargs:
                review = Optional(Uint32(kwargs["review_period_seconds"]))
            else:
                review = Optional(None)
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        (
                            "fee_paying_account",
                            ObjectId(kwargs["fee_paying_account"], "account"),
                        ),
                        ("expiration_time", PointInTime(kwargs["expiration_time"])),
                        (
                            "proposed_ops",
                            Array([Op_wrapper(o) for o in kwargs["proposed_ops"]]),
                        ),
                        ("review_period_seconds", review),
                        ("extensions", Set([])),
                    ]
                )
            )


class Proposal_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            for o in [
                "active_approvals_to_add",
                "active_approvals_to_remove",
                "owner_approvals_to_add",
                "owner_approvals_to_remove",
                "key_approvals_to_add",
                "key_approvals_to_remove",
            ]:
                if o not in kwargs:
                    kwargs[o] = []

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        (
                            "fee_paying_account",
                            ObjectId(kwargs["fee_paying_account"], "account"),
                        ),
                        ("proposal", ObjectId(kwargs["proposal"], "proposal")),
                        (
                            "active_approvals_to_add",
                            Array(
                                [
                                    ObjectId(o, "account")
                                    for o in kwargs["active_approvals_to_add"]
                                ]
                            ),
                        ),
                        (
                            "active_approvals_to_remove",
                            Array(
                                [
                                    ObjectId(o, "account")
                                    for o in kwargs["active_approvals_to_remove"]
                                ]
                            ),
                        ),
                        (
                            "owner_approvals_to_add",
                            Array(
                                [
                                    ObjectId(o, "account")
                                    for o in kwargs["owner_approvals_to_add"]
                                ]
                            ),
                        ),
                        (
                            "owner_approvals_to_remove",
                            Array(
                                [
                                    ObjectId(o, "account")
                                    for o in kwargs["owner_approvals_to_remove"]
                                ]
                            ),
                        ),
                        (
                            "key_approvals_to_add",
                            Array(
                                [PublicKey(o) for o in kwargs["key_approvals_to_add"]]
                            ),
                        ),
                        (
                            "key_approvals_to_remove",
                            Array(
                                [
                                    PublicKey(o)
                                    for o in kwargs["key_approvals_to_remove"]
                                ]
                            ),
                        ),
                        ("extensions", Set([])),
                    ]
                )
            )


class Proposal_delete(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('using_owner_authority', Bool(kwargs["using_owner_authority"])),
                ('proposal', ObjectId(kwargs["proposal"], "proposal")),
                ('extenstions', Set([])),
            ]))


class Sport_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            # Sort names by countrycode
            kwargs["name"] = sorted(
                kwargs["name"], key=lambda x: repr(x[0]), reverse=False
            )
            name = Map([[String(e[0]), String(e[1])] for e in kwargs["name"]])
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("name", name),
                        ("extensions", Set([])),
                    ]
                )
            )


class Sport_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "new_name" in kwargs:
                # Sort names by countrycode
                kwargs["new_name"] = sorted(
                    kwargs["new_name"], key=lambda x: repr(x[0]), reverse=False
                )
                name = Optional(
                    Map([[String(e[0]), String(e[1])] for e in kwargs["new_name"]])
                )
            else:
                name = Optional(None)
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("sport_id", ObjectId(kwargs["sport_id"], "sport")),
                        ("new_name", name),
                        ("extensions", Set([])),
                    ]
                )
            )


class Sport_delete(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("sport_id", ObjectId(kwargs["sport_id"], "sport")),
                        ("extensions", Set([])),
                    ]
                )
            )


class Sport_delete(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("sport_id", ObjectId(kwargs["sport_id"], "sport")),
                        ("extensions", Set([])),
                    ]
                )
            )


class Event_group_delete(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        (
                            "event_group_id",
                            ObjectId(kwargs["event_group_id"], "event_group"),
                        ),
                        ("extensions", Set([])),
                    ]
                )
            )


class Event_group_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            # Sort names by countrycode
            kwargs["name"] = sorted(
                kwargs["name"], key=lambda x: repr(x[0]), reverse=False
            )
            name = Map([[String(e[0]), String(e[1])] for e in kwargs["name"]])
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("name", name),
                        ("sport_id", FullObjectId(kwargs["sport_id"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Event_group_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "new_name" in kwargs:
                # Sort names by countrycode
                kwargs["new_name"] = sorted(
                    kwargs["new_name"], key=lambda x: repr(x[0]), reverse=False
                )
                name = Optional(
                    Map([[String(e[0]), String(e[1])] for e in kwargs["new_name"]])
                )
            else:
                name = Optional(None)

            if "new_sport_id" in kwargs:
                new_sport_id = Optional(FullObjectId(kwargs["new_sport_id"]))
            else:
                new_sport_id = Optional(None)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("new_sport_id", new_sport_id),
                        ("new_name", name),
                        (
                            "event_group_id",
                            ObjectId(kwargs["event_group_id"], "event_group"),
                        ),
                        ("extensions", Set([])),
                    ]
                )
            )


class Event_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            # Sort names by countrycode
            kwargs["name"] = sorted(
                kwargs.get("name", []), key=lambda x: repr(x[0]), reverse=False
            )
            name = Map([[String(e[0]), String(e[1])] for e in kwargs.get("name", [])])
            # Sort season by countrycode
            kwargs["season"] = sorted(
                kwargs.get("season", []), key=lambda x: repr(x[0]), reverse=False
            )
            season = Map(
                [[String(e[0]), String(e[1])] for e in kwargs.get("season", [])]
            )
            # Sort name by countrycode
            kwargs["name"] = sorted(
                kwargs.get("name", []), key=lambda x: repr(x[0]), reverse=False
            )
            name = Map([[String(e[0]), String(e[1])] for e in kwargs.get("name", [])])
            if "start_time" in kwargs:
                start_time = Optional(PointInTime(kwargs["start_time"]))
            else:
                start_time = Optional(None)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("name", name),
                        ("season", season),
                        ("start_time", start_time),
                        ("event_group_id", FullObjectId(kwargs["event_group_id"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Event_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            if "new_name" in kwargs:
                # Sort names by countrycode
                kwargs["new_name"] = sorted(
                    kwargs.get("new_name", []), key=lambda x: repr(x[0]), reverse=False
                )
                name = Optional(
                    Map(
                        [
                            [String(e[0]), String(e[1])]
                            for e in kwargs.get("new_name", [])
                        ]
                    )
                )
            else:
                name = Optional(None)

            if "new_season" in kwargs:
                # Sort season by countrycode
                kwargs["new_season"] = sorted(
                    kwargs.get("new_season", []),
                    key=lambda x: repr(x[0]),
                    reverse=False,
                )
                season = Optional(
                    Map(
                        [
                            [String(e[0]), String(e[1])]
                            for e in kwargs.get("new_season", [])
                        ]
                    )
                )
            else:
                season = Optional(None)

            if "new_name" in kwargs:
                # Sort name by countrycode
                kwargs["new_name"] = sorted(
                    kwargs.get("new_name", []), key=lambda x: repr(x[0]), reverse=False
                )
                name = Optional(
                    Map(
                        [
                            [String(e[0]), String(e[1])]
                            for e in kwargs.get("new_name", [])
                        ]
                    )
                )
            else:
                name = Optional(None)

            if "new_start_time" in kwargs:
                start_time = Optional(PointInTime(kwargs["new_start_time"]))
            else:
                start_time = Optional(None)

            if "new_status" in kwargs:
                status = Optional(EventStatus(kwargs["new_status"]))
            else:
                status = Optional(None)

            if "new_event_group_id" in kwargs:
                new_event_group_id = Optional(
                    FullObjectId(kwargs["new_event_group_id"])
                )
            else:
                new_event_group_id = Optional(None)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("event_id", ObjectId(kwargs["event_id"], "event")),
                        ("new_event_group_id", new_event_group_id),
                        ("new_name", name),
                        ("new_season", season),
                        ("new_start_time", start_time),
                        ("new_status", status),
                        ("extensions", Set([])),
                    ]
                )
            )


class Event_update_status(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            scores = [str(x) for x in kwargs["scores"]]

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("event_id", ObjectId(kwargs["event_id"], "event")),
                        ("status", EventStatus(kwargs["status"])),
                        ("scores", Array([String(o) for o in scores])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Betting_market_rules_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            # Sort names by countrycode
            kwargs["name"] = sorted(
                kwargs["name"], key=lambda x: repr(x[0]), reverse=False
            )
            name = Map([[String(e[0]), String(e[1])] for e in kwargs["name"]])
            # Sort description by countrycode
            kwargs["description"] = sorted(
                kwargs["description"], key=lambda x: repr(x[0]), reverse=False
            )
            description = Map(
                [[String(e[0]), String(e[1])] for e in kwargs["description"]]
            )
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("name", name),
                        ("description", description),
                        ("extensions", Set([])),
                    ]
                )
            )


class Betting_market_rules_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            if "new_name" in kwargs:
                # Sort names by countrycode
                kwargs["new_name"] = sorted(
                    kwargs["new_name"], key=lambda x: repr(x[0]), reverse=False
                )
                name = Optional(
                    Map([[String(e[0]), String(e[1])] for e in kwargs["new_name"]])
                )
            else:
                name = Optional(None)

            # Sort description by countrycode
            if "new_description" in kwargs:
                kwargs["new_description"] = sorted(
                    kwargs["new_description"], key=lambda x: repr(x[0]), reverse=False
                )
                description = Optional(
                    Map(
                        [
                            [String(e[0]), String(e[1])]
                            for e in kwargs["new_description"]
                        ]
                    )
                )
            else:
                description = Optional(None)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("new_name", name),
                        ("new_description", description),
                        ("extensions", Set([])),
                        (
                            "betting_market_rules_id",
                            ObjectId(
                                kwargs["betting_market_rules_id"],
                                "betting_market_rules",
                            ),
                        ),
                    ]
                )
            )


class Betting_market_group_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            # Sort description by countrycode
            kwargs["description"] = sorted(
                kwargs["description"], key=lambda x: repr(x[0]), reverse=False
            )
            description = Map(
                [[String(e[0]), String(e[1])] for e in kwargs["description"]]
            )
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("description", description),
                        ("event_id", FullObjectId(kwargs["event_id"])),
                        ("rules_id", FullObjectId(kwargs["rules_id"])),
                        ("asset_id", ObjectId(kwargs["asset_id"], "asset")),
                        ("never_in_play", Bool(kwargs["never_in_play"])),
                        (
                            "delay_before_settling",
                            Uint32(kwargs["delay_before_settling"]),
                        ),
                        ########################
                        # Multi Market Exposure
                        # Not available on beatrice or alice-hardfork
                        ########################
                        # (
                        #    "resolution_constraint",
                        #    ResolutionConstraint(kwargs["resolution_constraint"]),
                        # ),
                        ("extensions", Set([])),
                    ]
                )
            )


class Betting_market_group_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            if "new_description" in kwargs:
                # Sort description by countrycode
                kwargs["new_description"] = sorted(
                    kwargs["new_description"], key=lambda x: repr(x[0]), reverse=False
                )
                description = Optional(
                    Map(
                        [
                            [String(e[0]), String(e[1])]
                            for e in kwargs["new_description"]
                        ]
                    )
                )
            else:
                description = Optional(None)

            if "status" in kwargs:
                status = Optional(BettingMarketGroupStatus(kwargs["status"]))
            else:
                status = Optional(None)

            if "new_rules_id" in kwargs:
                new_rules_id = Optional(FullObjectId(kwargs["new_rules_id"]))
            else:
                new_rules_id = Optional(None)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        (
                            "betting_market_group_id",
                            ObjectId(
                                kwargs["betting_market_group_id"],
                                "betting_market_group",
                            ),
                        ),
                        ("new_description", description),
                        ("new_rules_id", new_rules_id),
                        ("status", status),
                        ("extensions", Set([])),
                    ]
                )
            )


class Betting_market_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            # Sort names by countrycode
            kwargs["payout_condition"] = sorted(
                kwargs.get("payout_condition", []),
                key=lambda x: repr(x[0]),
                reverse=False,
            )
            payout_condition = Map(
                [
                    [String(e[0]), String(e[1])]
                    for e in kwargs.get("payout_condition", [])
                ]
            )
            # Sort description by countrycode
            kwargs["description"] = sorted(
                kwargs["description"], key=lambda x: repr(x[0]), reverse=False
            )
            description = Map(
                [[String(e[0]), String(e[1])] for e in kwargs["description"]]
            )

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("group_id", FullObjectId(kwargs["group_id"])),
                        ("description", description),
                        ("payout_condition", payout_condition),
                        ("extensions", Set([])),
                    ]
                )
            )


class Betting_market_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            # Sort names by countrycode
            if "new_payout_condition" in kwargs:
                kwargs["new_payout_condition"] = sorted(
                    kwargs.get("new_payout_condition", []),
                    key=lambda x: repr(x[0]),
                    reverse=False,
                )
                payout_condition = Optional(
                    Map(
                        [
                            [String(e[0]), String(e[1])]
                            for e in kwargs.get("new_payout_condition", [])
                        ]
                    )
                )
            else:
                payout_condition = Optional(None)

            if "new_description" in kwargs:
                # Sort description by countrycode
                kwargs["new_description"] = sorted(
                    kwargs["new_description"], key=lambda x: repr(x[0]), reverse=False
                )
                description = Optional(
                    Map(
                        [
                            [String(e[0]), String(e[1])]
                            for e in kwargs["new_description"]
                        ]
                    )
                )
            else:
                description = Optional(None)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        (
                            "betting_market_id",
                            ObjectId(kwargs["betting_market_id"], "betting_market"),
                        ),
                        (
                            "new_group_id",
                            Optional(FullObjectId(kwargs["new_group_id"])),
                        ),
                        ("new_description", description),
                        ("new_payout_condition", payout_condition),
                        ("extensions", Set([])),
                    ]
                )
            )


class Betting_market_group_resolve(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        (
                            "betting_market_group_id",
                            ObjectId(
                                kwargs["betting_market_group_id"],
                                "betting_market_group",
                            ),
                        ),
                        (
                            "resolutions",
                            Map(
                                [
                                    [
                                        ObjectId(o[0], "betting_market"),
                                        BettingMarketResolution(o[1]),
                                    ]
                                    for o in sorted(
                                        kwargs["resolutions"],
                                        key=(lambda x: int(x[0].split(".")[2])),
                                    )
                                ]
                            ),
                        ),
                        ("extensions", Set([])),
                    ]
                )
            )


class Bet_place(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("bettor_id", ObjectId(kwargs["bettor_id"], "account")),
                        (
                            "betting_market_id",
                            ObjectId(kwargs["betting_market_id"], "betting_market"),
                        ),
                        ("amount_to_bet", Asset(kwargs["amount_to_bet"])),
                        ("backer_multiplier", Uint32(int(kwargs["backer_multiplier"]))),
                        ("back_or_lay", BetType(kwargs["back_or_lay"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Bet_cancel(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("bettor_id", ObjectId(kwargs["bettor_id"], "account")),
                        # ("bet_to_cancel", ObjectId(kwargs["bet_to_cancel"], "bet")),
                        ("bet_to_cancel", ObjectId(kwargs["bet_to_cancel"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Tournament_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("creator", ObjectId(kwargs["creator"], "account")),
                        ("options", TournamentOptions(kwargs["options"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Tournament_join(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        (
                            "payer_account_id",
                            ObjectId(kwargs["payer_account_id"], "account"),
                        ),
                        (
                            "player_account_id",
                            ObjectId(kwargs["player_account_id"], "account"),
                        ),
                        (
                            "tournament_id",
                            ObjectId(kwargs["tournament_id"], "tournament"),
                        ),
                        ("buy_in", Asset(kwargs["buy_in"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Tournament_leave(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        (
                            "canceling_account_id",
                            ObjectId(kwargs["canceling_account_id"], "account"),
                        ),
                        (
                            "player_account_id",
                            ObjectId(kwargs["player_account_id"], "account"),
                        ),
                        (
                            "tournament_id",
                            ObjectId(kwargs["tournament_id"], "tournament"),
                        ),
                        ("extensions", Set([])),
                    ]
                )
            )


class Game_move(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("game_id", ObjectId(kwargs["game_id"], "game")),
                        (
                            "player_account_id",
                            ObjectId(kwargs["player_account_id"], "account"),
                        ),
                        ("move", GameSpecificMoves(kwargs["move"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Balance_claim(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        (
                            "deposit_to_account",
                            ObjectId(kwargs["deposit_to_account"], "account"),
                        ),
                        (
                            "balance_to_claim",
                            ObjectId(kwargs["balance_to_claim"], "balance"),
                        ),
                        (
                            "balance_owner_key",
                            PublicKey(kwargs["balance_owner_key"], prefix=prefix),
                        ),
                        ("total_claimed", Asset(kwargs["total_claimed"])),
                    ]
                )
            )


class Custom_permission_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("owner_account", ObjectId(kwargs["owner_account"], "account")),
                        ("permission_name", String(kwargs["permission_name"])),
                        ("auth", Permission(kwargs["auth"], prefix=prefix)),
                        ("extensions", Set([])),
                    ]
                )
            )


class Custom_permission_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("permission_id", ObjectId(kwargs["permission_id"], "custom_permission")),
                        ("new_auth", Optional(Permission(kwargs["new_auth"], prefix=prefix))),
                        ("owner_account", ObjectId(kwargs["owner_account"], "account")),
                    ]
                )
            )


class Custom_permission_delete(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("permission_id", ObjectId(kwargs["permission_id"], "custom_permission")),
                        ("owner_account", ObjectId(kwargs["owner_account"], "account")),
                    ]
                )
            )


class Custom_account_authority_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("permission_id", ObjectId(kwargs["permission_id"], "custom_permission")),
                        ("operation_type", Uint32(kwargs["operation_type"])),
                        ("valid_from", PointInTime(kwargs["valid_from"])),
                        ("valid_to", PointInTime(kwargs["valid_to"])),
                        ("owner_account", ObjectId(kwargs["owner_account"], "account")),
                    ]
                )
            )


class Custom_account_authority_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("auth_id", ObjectId(kwargs["auth_id"], "custom_account_authority")),
                        ("new_valid_from", Optional(PointInTime(kwargs["new_valid_from"]))),
                        ("new_valid_to", Optional(PointInTime(kwargs["new_valid_to"]))),
                        ("owner_account", ObjectId(kwargs["owner_account"], "account")),
                    ]
                )
            )


class Custom_account_authority_delete(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("auth_id", ObjectId(kwargs["auth_id"], "custom_account_authority")),
                        ("owner_account", ObjectId(kwargs["owner_account"], "account")),
                    ]
                )
            )


# ----------------------------------------
#       Market Place Classes
# ----------------------------------------

class Offer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            for o in [
                    "item_ids",
                    ]:
                if o not in kwargs:
                    kwargs[o] = []

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        # ("item_ids", Set([ObjectId(kwargs["item_ids"])])),
                        # ("item_ids", Set([ObjectId(item_ids)])),
                        (
                            "item_ids",
                            Array(
                                [
                                    ObjectId(o)
                                    for o in kwargs["item_ids"]
                                ]
                            ),
                        ),
                        ("issuer", ObjectId(kwargs["issuer"], "account")),
                        ("minimum_price", Asset(kwargs["minimum_price"])),
                        ("maximum_price", Asset(kwargs["maximum_price"])),
                        ("buying_item", Bool(kwargs["buying_item"])),
                        ("offer_expiration_date", PointInTime(kwargs["offer_expiration_date"])),
                        ("memo", Optional(None)), 
                        ("extensions", Set([])),
                    ]
                )
            )


class Bid(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("bidder", ObjectId(kwargs["bidder"], "account")),
                        ("bid_price", Asset(kwargs["bid_price"])),
                        ("offer_id", ObjectId(kwargs["offer_id"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Cancel_offer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("issuer", ObjectId(kwargs["issuer"], "account")),
                        ("offer_id", ObjectId(kwargs["offer_id"])),
                        ("extensions", Set([])),
                    ]
                )
            )


# ----------------------------------------
#       NFT Operations Classes
# ----------------------------------------

class Nft_metadata_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            if "revenue_partenr" in kwargs.keys():
                if not isinstance(kwargs["revenue_partner"], type(None)):
                    revenue_partner = Optional(ObjectId(kwargs["revenue_partner"], "account"))
                    revenue_split = Optional(Uint16(kwargs["revenue_split"]))
            else:
                revenue_partner = Optional(None)
                revenue_split = Optional(None)

            role_id = Optional(None)
            max_supply = Optional(None)
            lottery_options = Optional(None)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("owner", ObjectId(kwargs["owner"], "account")),
                        ("name", String(kwargs["name"])),
                        ("symbol", String(kwargs["symbol"])),
                        ("base_uri", String(kwargs["base_uri"])),
                        ("revenue_partner", revenue_partner),
                        ("revenue_split", revenue_split),
                        ("is_transferable", Bool(bool(kwargs["is_transferable"]))),
                        ("is_sellable", Bool(bool(kwargs["is_sellable"]))),
                        ("role_id", role_id),
                        ("max_supply", max_supply),
                        ("lottery_options", lottery_options),
                        ("extensions", Set([])),
                    ]
                )
            )


class Nft_metadata_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            if "revenue_partenr" in kwargs.keys():
                if not isinstance(kwargs["revenue_partner"], type(None)):
                    revenue_partner = Optional(ObjectId(kwargs["revenue_partner"], "account"))
                    revenue_split = Optional(Uint16(kwargs["revenue_split"]))
            else:
                revenue_partner = Optional(None)
                revenue_split = Optional(None)

            role_id = Optional(None)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("owner", ObjectId(kwargs["owner"], "account")),
                        ("nft_metadata_id", ObjectId(kwargs["nft_metadata_id"])),
                        ("name", Optional(String(kwargs["name"]))),
                        ("symbol", Optional(String(kwargs["symbol"]))),
                        ("base_uri", Optional(String(kwargs["base_uri"]))),
                        ("revenue_partner", revenue_partner),
                        ("revenue_split", revenue_split),
                        ("is_transferable", Optional(Bool(kwargs["is_transferable"]))),
                        ("is_sellable", Optional(Bool(kwargs["is_sellable"]))),
                        ("role_id", role_id),
                        ("extensions", Set([])),
                    ]
                )
            )


class Nft_mint(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("payer", ObjectId(kwargs["payer"], "account")),
                        ("nft_metadata_id", ObjectId(kwargs["nft_metadata_id"])),
                        ("owner", ObjectId(kwargs["owner"], "account")),
                        ("approved", ObjectId(kwargs["approved"], "account")),
                        ("approved_operators", Set([])),
                        ("token_uri", String(kwargs["token_uri"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Nft_safe_transfer_from(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("operator_", ObjectId(kwargs["operator_"], "account")),
                        ("from", ObjectId(kwargs["from"], "account")),
                        ("to", ObjectId(kwargs["to"], "account")),
                        ("token_id", ObjectId(kwargs["token_id"])),
                        ("data", String(kwargs["data"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Nft_approve(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("operator_", ObjectId(kwargs["operator_"], "account")),
                        ("approved", ObjectId(kwargs["approved"], "account")),
                        ("token_id", ObjectId(kwargs["token_id"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class Nft_set_approval_for_all(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("owner", ObjectId(kwargs["owner"], "account")),
                        ("operator_", ObjectId(kwargs["operator_"], "account")),
                        ("approved", Bool(kwargs["approved"])),
                        ("extensions", Set([])),
                    ]
                )
            )
            

class Custom_permission_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("permission_id", ObjectId(kwargs["permission_id"], "custom_permission")),
                        ("new_auth", Optional(Permission(kwargs["new_auth"], prefix=prefix))),
                        ("owner_account", ObjectId(kwargs["owner_account"], "account")),
                        ("extensions", Set([])),
                    ]
                )
            )


class Custom_permission_delete(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)
            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("permission_id", ObjectId(kwargs["permission_id"], "custom_permission")),
                        ("owner_account", ObjectId(kwargs["owner_account"], "account")),
                        ("extensions", Set([])),
                    ]
                )
            )


class Custom_account_authority_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("permission_id", ObjectId(kwargs["permission_id"], "custom_permission")),
                        ("operation_type", Uint32(kwargs["operation_type"])),
                        ("valid_from", PointInTime(kwargs["valid_from"])),
                        ("valid_to", PointInTime(kwargs["valid_to"])),
                        ("owner_account", ObjectId(kwargs["owner_account"], "account")),
                        ("extensions", Set([])),
                    ]
                )
            )


class Custom_account_authority_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("auth_id", ObjectId(kwargs["auth_id"], "custom_account_authority")),
                        ("new_valid_from", Optional(PointInTime(kwargs["new_valid_from"]))),
                        ("new_valid_to", Optional(PointInTime(kwargs["new_valid_to"]))),
                        ("owner_account", ObjectId(kwargs["owner_account"], "account")),
                        ("extensions", Set([])),
                    ]
                )
            )


class Custom_account_authority_delete(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(
                OrderedDict(
                    [
                        ("fee", Asset(kwargs["fee"])),
                        ("auth_id", ObjectId(kwargs["auth_id"], "custom_account_authority")),
                        ("owner_account", ObjectId(kwargs["owner_account"], "account")),
                        ("extensions", Set([])),
                    ]
                )
            )
