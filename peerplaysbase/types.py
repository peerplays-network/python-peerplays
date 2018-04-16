from binascii import unhexlify
from graphenebase.types import varint


def zigzag_encode(i):
    return (i >> 31) ^ (i << 1)


def zigzag_decode(i):
    return (i >> 1) ^ -(i & 1)


class Signed_Int():
    def __init__(self, d):
        self.data = int(d)

    def __bytes__(self):
        return varint(zigzag_encode(self.data))

    def __str__(self):
        return '%d' % self.data


class Enum(Signed_Int):
    def __init__(self, selection):
        assert selection in self.options or \
            isinstance(selection, int) and len(self.options) < selection, \
            "Options are %s. Given '%s'" % (
                self.options, selection)
        if selection in self.options:
            super().__init__(self.options.index(selection))
        else:
            super().__init__(selection)

    def __str__(self):
        return str(self.options[self.data])


class Sha256():
    def __init__(self, d):
        self.data = d
        assert len(self.data) == 64

    def __bytes__(self):
        return unhexlify(bytes(self.data, 'ascii'))

    def __str__(self):
        return str(self.data)
