# -*- coding: utf-8 -*-
from .exceptions import ObjectNotInProposalBuffer
from .instance import BlockchainInstance

# Load methods from graphene and provide them to bitshares
from graphenecommon.utils import (
    formatTime,
    timeFormat,
    formatTimeString,
    formatTimeFromNow,
    parse_time,
    assets_from_string,
)


def test_proposal_in_buffer(buf, operation_name, id):
    from .transactionbuilder import ProposalBuilder
    from peerplaysbase.operationids import operations

    assert isinstance(buf, ProposalBuilder)

    operationid = operations.get(operation_name)
    _, _, j = id.split(".")

    ops = buf.list_operations()
    if len(ops) <= int(j):
        raise ObjectNotInProposalBuffer(
            "{} with id {} not found".format(operation_name, id)
        )
    op = ops[int(j)].json()
    if op[0] != operationid:
        raise ObjectNotInProposalBuffer(
            "{} with id {} not found".format(operation_name, id)
        )


def map2dict(darray):
    """ Reformat a list of maps to a dictionary
    """
    return {v[0]: v[1] for v in darray}
