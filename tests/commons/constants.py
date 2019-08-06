import os

from preptools.utils.constants import PROJECT_ROOT_PATH

TEST_DIRECTORY = os.path.abspath(os.path.join(PROJECT_ROOT_PATH, 'tests'))
TEST_UTIL_DIRECTORY = os.path.join(TEST_DIRECTORY, 'commons')
IN_MEMORY_ZIP_TEST_DIRECTORY = os.path.join(TEST_UTIL_DIRECTORY, 'test_in_memory_zip')

TEST_CONFIG_PATH = os.path.join(TEST_UTIL_DIRECTORY, 'preptools_config.json')
TEST_KEYSTORE_PATH = os.path.join(TEST_UTIL_DIRECTORY, 'test_keystore')
TEST_KEYSTORE_PASSWORD = 'qwer1234%'
TEST_REGISTER_JSON_PATH = os.path.join(TEST_UTIL_DIRECTORY, 'registerPRep.json')
TEST_SET_JSON_PATH = os.path.join(TEST_UTIL_DIRECTORY, 'setPRep.json')

register_sample = {
    "from_": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
    "to": "cx0000000000000000000000000000000000000000",
    "value": 2000000000000000000000,
    "step_limit": 268435456,
    "nid": 3,
    "nonce": None,
    "version": 3,
    "timestamp": None,
    "method": "registerPRep",
    "data_type": "call",
    "params": {
        "name": "banana node",
        "country": "KOR",
        "city": "Seoul",
        "email": "banana@example.com",
        "website": "https://icon.banana.com",
        "details": "https://icon.banana.com/json",
        "p2pEndpoint": "node.example.com:7100"
    }
}

set_sample = {
    "from_": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
    "to": "cx0000000000000000000000000000000000000000",
    "value": 0,
    "step_limit": 268435456,
    "nid": 3,
    "nonce": None,
    "version": 3,
    "timestamp": None,
    "method": "setPRep",
    "data_type": "call",
    "params": {
        "name": "kokoa node",
        "country": "KOR",
        "website": "https://icon.kokoa.com",
        "details": "https://icon.kokoa.com/json",
        "p2pEndpoint": "node.example.com:7100"
    }
}

unregister_sample = {
    "from_": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
    "to": "cx0000000000000000000000000000000000000000",
    "value": 0,
    "step_limit": 268435456,
    "nid": 3,
    "nonce": None,
    "version": 3,
    "timestamp": None,
    "method": "unregisterPRep",
    "data_type": "call",
    "params": {}
}

set_governance_variables_sample = {
    "from_": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
    "to": "cx0000000000000000000000000000000000000000",
    "value": 0,
    "step_limit": 268435456,
    "nid": 3,
    "nonce": None,
    "version": 3,
    "timestamp": None,
    "method": "setGovernanceVariables",
    "data_type": "call",
    "params": {
        "irep": "0x30"
    }
}

get_prep_sample = {
    "from_": "hx1234567890123456789012345678901234567890",
    "to": "cx0000000000000000000000000000000000000000",
    "method": "getPRep",
    "params": {
        "address": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6"
    }
}

get_preps_sample = {
    "from_": "hx1234567890123456789012345678901234567890",
    "to": "cx0000000000000000000000000000000000000000",
    "method": "getPReps",
    "params": None
}
