from .peerplays import PeerPlays
from graphenebase import base58

__all__ = [
    "account",
    "aes",
    "amount",
    "asset",
    "bet",
    "bettingmarket",
    "bettingmarketgroup",
    "block",
    "blockchain",
    "committee",
    "event",
    "eventgroup",
    "exceptions",
    "instance",
    "memo",
    "peerplays",
    "proposal",
    "sport",
    "storage",
    "transactionbuilder",
    "utils",
    "wallet",
    "witness",
    "notify",
]
base58.known_prefixes.append("PPY")
base58.known_prefixes.append("PPY1")
base58.known_prefixes.append("PPYTEST")

GRAPHENE_BETTING_ODDS_PRECISION = 10000

SIGNED_MESSAGE_META = """{message}
-----BEGIN META-----
account={meta[account]}
memokey={meta[memokey]}
block={meta[block]}
timestamp={meta[timestamp]} """

SIGNED_MESSAGE_ENCAPSULATED = """
-----BEGIN BITSHARES SIGNED MESSAGE-----
{message}
-----BEGIN SIGNATURE-----
{signature}
-----END BITSHARES SIGNED MESSAGE-----"""
