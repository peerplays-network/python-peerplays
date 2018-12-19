# -*- coding: utf-8 -*-
from .instance import BlockchainInstance
from graphenecommon.blockchainobject import (
    BlockchainObject as GrapheneBlockchainObject,
    BlockchainObjects as GrapheneBlockchainObjects,
    ObjectCache,
)


@BlockchainInstance.inject
class BlockchainObject(GrapheneBlockchainObject):
    pass


@BlockchainInstance.inject
class BlockchainObjects(GrapheneBlockchainObjects):
    pass
