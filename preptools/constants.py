__all__ = (
    "get_predefined_address",
    "get_predefined_nid",
    "get_predefined_url",
)

from typing import (
    Optional,
    Tuple,
)


# api endpoint and nid
_PREDEFINED_URLS = {
    "berlin": ("https://berlin.net.solidwallet.io/api/v3", 7),
    "lisbon": ("https://lisbon.net.solidwallet.io/api/v3", 2),
    "mainnet": ("https://ctz.solidwallet.io/api/v3", 1),
}

SYSTEM_SCORE_ADDRESS = "cx0000000000000000000000000000000000000000"
GOVERNANCE_SCORE_ADDRESS = "cx0000000000000000000000000000000000000001"
TREASURY_ADDRESS = "hx1000000000000000000000000000000000000000"

_PREDEFINED_ADDRESSES = {
    "governance": GOVERNANCE_SCORE_ADDRESS,
    "gov": GOVERNANCE_SCORE_ADDRESS,
    "chain": SYSTEM_SCORE_ADDRESS,
    "system": SYSTEM_SCORE_ADDRESS,
    "sys": SYSTEM_SCORE_ADDRESS,
    "treasury": TREASURY_ADDRESS,
}


def get_predefined_url(name: str) -> Optional[str]:
    info = _PREDEFINED_URLS.get(name)
    if info is None:
        return None
    return info[0]


def get_predefined_nid(name: str) -> int:
    info = _PREDEFINED_URLS.get(name)
    if info is None:
        return 0
    return info[1]


def get_predefined_address(name: str) -> Optional[str]:
    return _PREDEFINED_ADDRESSES.get(name)
