# -*- coding: utf-8 -*-
from peerplaysbase.account import PrivateKey, PublicKey
from .account import Account
from .instance import BlockchainInstance

from graphenecommon.memo import Memo as GrapheneMemo


@BlockchainInstance.inject
class Memo(GrapheneMemo):
    """ Deals with Memos that are attached to a transfer

        :param peerplays.account.Account from_account: Account that has sent
            the memo
        :param peerplays.account.Account to_account: Account that has received
            the memo
        :param peerplays.peerplays.PeerPlays blockchain_instance: instance

        A memo is encrypted with a shared secret derived from a private key of
        the sender and a public key of the receiver. Due to the underlying
        mathematics, the same shared secret can be derived by the private key
        of the receiver and the public key of the sender. The encrypted message
        is perturbed by a nonce that is part of the transmitted message.

        .. code-block:: python

            from peerplays.memo import Memo
            m = Memo("from", "to")
            m.unlock_wallet("secret")
            enc = (m.encrypt("foobar"))
            print(enc)
            >> {'nonce': '17329630356955254641', 'message': '8563e2bb2976e0217806d642901a2855'}
            print(m.decrypt(enc))
            >> foobar

        To decrypt a memo, simply use

        .. code-block:: python

            from peerplays.memo import Memo
            m = Memo()
            m.blockchain.wallet.unlock("secret")
            print(memo.decrypt(op_data["memo"]))

        if ``op_data`` being the payload of a transfer operation.

    """

    MESSAGE_SPLIT = (
        "-----BEGIN PEERPLAYS SIGNED MESSAGE-----",
        "-----BEGIN META-----",
        "-----BEGIN SIGNATURE-----",
        "-----END PEERPLAYS SIGNED MESSAGE-----",
    )

    def define_classes(self):
        self.account_class = Account
        self.privatekey_class = PrivateKey
        self.publickey_class = PublicKey
