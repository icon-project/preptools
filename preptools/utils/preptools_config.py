from preptools.utils.constants import DEFAULT_URL, DEFAULT_NID

FN_CLI_CONF = './preptools_config.json'

preptools_config = {
    "url": DEFAULT_URL,
    "nid": DEFAULT_NID,
    "keystore": None
}


def get_default_config():
    return preptools_config
