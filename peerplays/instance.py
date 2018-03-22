import peerplays as ppy


class SharedInstance():
    instance = None
    config = {}


def shared_peerplays_instance():
    """ This method will initialize ``SharedInstance.instance`` and return it.
        The purpose of this method is to have offer single default
        peerplays instance that can be reused by multiple classes.
    """
    if not SharedInstance.instance:
        clear_cache()
        SharedInstance.instance = ppy.PeerPlays(**SharedInstance.config)
    return SharedInstance.instance


def set_shared_peerplays_instance(peerplays_instance):
    """ This method allows us to override default peerplays instance for all
        users of ``SharedInstance.instance``.

        :param peerplays.Peerplays peerplays_instance: Peerplays
            instance
    """
    clear_cache()
    SharedInstance.instance = peerplays_instance


def clear_cache():
    """ Clear Caches
    """
    from .blockchainobject import BlockchainObject
    BlockchainObject.clear_cache()


def set_shared_config(config):
    """ This allows to set a config that will be used when calling
        ``shared_peerplays_instance`` and allows to define the configuration
        without requiring to actually create an instance
    """
    assert isinstance(config, dict)
    SharedInstance.config = config
