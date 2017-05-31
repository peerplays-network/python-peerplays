from collections import OrderedDict
import json
from graphenebase.types import (
    Uint8, Int16, Uint16, Uint32, Uint64,
    Varint32, Int64, String, Bytes, Void,
    Array, PointInTime, Signature, Bool,
    Set, Fixed_array, Optional, Static_variant,
    Map, Id, VoteId, FullObjectId
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
    BettingMarketOptions,
    BetType,
    BettingMarketResolution
)
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
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('from', ObjectId(kwargs["from"], "account")),
                ('to', ObjectId(kwargs["to"], "account")),
                ('amount', Asset(kwargs["amount"])),
                ('memo', memo),
                ('extensions', Set([])),
            ]))


class Account_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('registrar', ObjectId(kwargs["registrar"], "account")),
                ('referrer', ObjectId(kwargs["referrer"], "account")),
                ('referrer_percent', Uint16(kwargs["referrer_percent"])),
                ('name', String(kwargs["name"])),
                ('owner', Permission(kwargs["owner"], prefix=prefix)),
                ('active', Permission(kwargs["active"], prefix=prefix)),
                ('options', AccountOptions(kwargs["options"], prefix=prefix)),
                ('extensions', Set([])),
            ]))


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
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('account', ObjectId(kwargs["account"], "account")),
                ('owner', owner),
                ('active', active),
                ('new_options', options),
                ('extensions', Set([])),
            ]))


class Account_upgrade(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('account_to_upgrade', ObjectId(kwargs["account_to_upgrade"], "account")),
                ('upgrade_to_lifetime_member', Bool(kwargs["upgrade_to_lifetime_member"])),
                ('extensions', Set([])),
            ]))


class Op_wrapper(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('op', Operation(kwargs["op"])),
            ]))


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
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('expiration_time', PointInTime(kwargs["expiration_time"])),
                ('proposed_ops',
                    Array([Op_wrapper(o) for o in kwargs["proposed_ops"]])),
                ('review_period_seconds', review),
                ('extensions', Set([])),
            ]))


class Proposal_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            for o in ['active_approvals_to_add',
                      'active_approvals_to_remove',
                      'owner_approvals_to_add',
                      'owner_approvals_to_remove',
                      'key_approvals_to_add',
                      'key_approvals_to_remove']:
                if o not in kwargs:
                    kwargs[o] = []

            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('proposal', ObjectId(kwargs["proposal"], "proposal")),
                ('active_approvals_to_add',
                    Array([ObjectId(o, "account") for o in kwargs["active_approvals_to_add"]])),
                ('active_approvals_to_remove',
                    Array([ObjectId(o, "account") for o in kwargs["active_approvals_to_remove"]])),
                ('owner_approvals_to_add',
                    Array([ObjectId(o, "account") for o in kwargs["owner_approvals_to_add"]])),
                ('owner_approvals_to_remove',
                    Array([ObjectId(o, "account") for o in kwargs["owner_approvals_to_remove"]])),
                ('key_approvals_to_add',
                    Array([PublicKey(o) for o in kwargs["key_approvals_to_add"]])),
                ('key_approvals_to_remove',
                    Array([PublicKey(o) for o in kwargs["key_approvals_to_remove"]])),
                ('extensions', Set([])),
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
                kwargs["name"],
                key=lambda x: repr(x[0]),
                reverse=False,
            )
            name = Map([
                [String(e[0]), String(e[1])]
                for e in kwargs["name"]
            ])
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('name', name),
                ('extensions', Set([])),
            ]))


class Competitor_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            # Sort names by countrycode
            kwargs["name"] = sorted(
                kwargs["name"],
                key=lambda x: repr(x[0]),
                reverse=False,
            )
            name = Map([
                [String(e[0]), String(e[1])]
                for e in kwargs["name"]
            ])
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('name', name),
                ('sport_id', FullObjectId(kwargs["sport_id"])),
                ('extensions', Set([])),
            ]))


class Event_group_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            # Sort names by countrycode
            kwargs["name"] = sorted(
                kwargs["name"],
                key=lambda x: repr(x[0]),
                reverse=False,
            )
            name = Map([
                [String(e[0]), String(e[1])]
                for e in kwargs["name"]
            ])
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('name', name),
                ('sport_id', FullObjectId(kwargs["sport_id"])),
                ('extensions', Set([])),
            ]))


class Event_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            # Sort names by countrycode
            kwargs["name"] = sorted(
                kwargs.get("name", []),
                key=lambda x: repr(x[0]),
                reverse=False,
            )
            name = Map([
                [String(e[0]), String(e[1])]
                for e in kwargs.get("name", [])
            ])
            # Sort season by countrycode
            kwargs["season"] = sorted(
                kwargs.get("season", []),
                key=lambda x: repr(x[0]),
                reverse=False,
            )
            season = Map([
                [String(e[0]), String(e[1])]
                for e in kwargs.get("season", [])
            ])
            if "start_time" in kwargs:
                start_time = Optional(PointInTime(kwargs["start_time"]))
            else:
                start_time = Optional(None)

            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('name', name),
                ('season', season),
                ('start_time', start_time),
                ('event_group_id', FullObjectId(kwargs["event_group_id"])),
                ('competitors',
                    Array([FullObjectId(o) for o in kwargs["competitors"]])),
                ('extensions', Set([])),
            ]))


class Betting_market_group_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('event_id', FullObjectId(kwargs["event_id"])),
                ('options', BettingMarketOptions(kwargs["options"])),
                ('extensions', Set([])),
            ]))


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
            payout_condition = Map([
                [String(e[0]), String(e[1])]
                for e in kwargs.get("payout_condition", [])
            ])
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('group_id', FullObjectId(kwargs["group_id"])),
                ('payout_condition', payout_condition),
                ('asset_id', ObjectId(kwargs["asset_id"], "asset")),
                ('extensions', Set([])),
            ]))


class Bet_place(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('bettor_id', ObjectId(kwargs["bettor_id"], "account")),
                ('betting_market_id', ObjectId(kwargs["betting_market_id"], "betting_market")),
                ('amount_to_bet', Asset(kwargs["amount_to_bet"])),
                ('backer_multiplier', Uint32(int(kwargs["backer_multiplier"]))),
                ('amount_reserved_for_fees', Int64(kwargs["amount_reserved_for_fees"])),
                ('back_or_lay', BetType(kwargs["back_or_lay"])),
                ('extensions', Set([])),
            ]))


class Betting_market_resolve(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('betting_market_id', ObjectId(kwargs["betting_market_id"], "betting_market")),
                ('resolution', BettingMarketResolution(kwargs["resolution"])),
                ('extensions', Set([])),
            ]))


class Bet_cancel(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            # FIXME: this serialization does not work properly yet
            raise NotImplementedError

            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('bettor_id', ObjectId(kwargs["bettor_id"], "account")),
                ('bet_to_cancel', ObjectId(kwargs["bet_to_cancel"], "bet")),
                ('extensions', Set([])),
            ]))
