import peerplays as ppy

_shared_peerplays_instance = None


def shared_peerplays_instance():
    """ This method will initialize ``_shared_peerplays_instance`` and return it.
        The purpose of this method is to have offer single default
        peerplays instance that can be reused by multiple classes.
    """
    global _shared_peerplays_instance
    if not _shared_peerplays_instance:
        _shared_peerplays_instance = ppy.PeerPlays()
    return _shared_peerplays_instance


def set_shared_peerplays_instance(peerplays_instance):
    """ This method allows us to override default peerplays instance for all users of
        ``_shared_peerplays_instance``.

        :param peerplays.peerplays.PeerPlays peerplays_instance: PeerPlays instance
    """
    global _shared_peerplays_instance
    _shared_peerplays_instance = peerplays_instance
