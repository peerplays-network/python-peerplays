from peerplays.instance import shared_peerplays_instance


class BlockchainObject(dict):

    _cache = dict()

    def __init__(
        self,
        data,
        *args,
        klass=None,
        space_id=1,
        object_id=None,
        lazy=True,
        use_cache=True,
        peerplays_instance=None,
        **kwargs,
    ):
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.cached = False
        self.identifier = None

        if klass and isinstance(data, klass):
            self.identifier = data.get("id")
            super().__init__(data)
        elif isinstance(data, dict):
            self.identifier = data.get("id")
            super().__init__(data)
        else:
            self.identifier = data
            if self.iscached(data):
                super().__init__(self.getcache(data))
            elif not lazy and not self.cached:
                self.refresh()

        if use_cache and not lazy:
            self.cache(self)
            self.cached = True

    def cache(self, data):
        # store in cache
        if "id" in data:
            BlockchainObject._cache[data.get("id")] = data

    def iscached(self, id):
        return id in BlockchainObject._cache

    def getcache(self, id):
        return BlockchainObject._cache.get(id, None)

    def __getitem__(self, key):
        if not self.cached:
            self.refresh()
        return super().__getitem__(key)

    def items(self):
        if not self.cached:
            self.refresh()
        return super().items()

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self.identifier))
