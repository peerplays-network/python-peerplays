# -*- coding: utf-8 -*-
from graphenecommon.instance import AbstractBlockchainInstanceProvider, SharedInstance


class BlockchainInstance(AbstractBlockchainInstanceProvider):
    """ This is a class that allows compatibility with previous
        naming conventions
    """

    def __init__(self, *args, **kwargs):
        # Also allow 'peerplays_instance'
        if kwargs.get("peerplays_instance"):
            kwargs["blockchain_instance"] = kwargs["peerplays_instance"]
        if kwargs.get("blockchain_instance"):
            SharedInstance.instance = kwargs["blockchain_instance"]

    def get_instance_class(self):
        """ Should return the Chain instance class, e.g. `peerplays.PeerPlays`
        """
        import peerplays as ppy

        return ppy.PeerPlays

    @property
    def peerplays(self):
        """ Alias for the specific blockchain
        """
        return self.blockchain


def shared_blockchain_instance():
    return BlockchainInstance().shared_blockchain_instance()


def set_shared_blockchain_instance(instance):
    # clear cache
    inst = shared_blockchain_instance()
    inst.clear_cache()
    BlockchainInstance().set_shared_blockchain_instance(instance)


def set_shared_config(config):
    shared_blockchain_instance().set_shared_config(config)


shared_peerplays_instance = shared_blockchain_instance
set_shared_peerplays_instance = set_shared_blockchain_instance
