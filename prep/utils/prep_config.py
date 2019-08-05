from prep.utils.constants import DEFAULT_URL, DEFAULT_NID
from iconsdk.utils.convert_type import convert_int_to_hex_str

preptools_config = {
    "url": DEFAULT_URL,
    "nid": DEFAULT_NID,
    "keystore": None
}


def get_default_config():
    return preptools_config

