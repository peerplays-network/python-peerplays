from graphenestorage import (
    InRamConfigurationStore,
    InRamEncryptedKeyStore,
    InRamPlainKeyStore,
    SqliteConfigurationStore,
    SqliteEncryptedKeyStore,
    SQLiteFile,
    SqlitePlainKeyStore,
)


# url = "wss://"
# InRamConfigurationStore.setdefault("node", url)
# SqliteConfigurationStore.setdefault("node", url)


def get_default_config_store(*args, **kwargs):
    if "appname" not in kwargs:
        kwargs["appname"] = "peerplays"
    return SqliteConfigurationStore(*args, **kwargs)


def get_default_key_store(config, *args, **kwargs):
    if "appname" not in kwargs:
        kwargs["appname"] = "peerplays"
    return SqliteEncryptedKeyStore(config=config, **kwargs)
