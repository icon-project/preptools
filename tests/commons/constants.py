import os

from preptools.utils.constants import PROJECT_ROOT_PATH

TEST_DIRECTORY = os.path.abspath(os.path.join(PROJECT_ROOT_PATH, 'tests'))
TEST_UTIL_DIRECTORY = os.path.join(TEST_DIRECTORY, 'commons')
IN_MEMORY_ZIP_TEST_DIRECTORY = os.path.join(TEST_UTIL_DIRECTORY, 'test_in_memory_zip')

TEST_CONFIG_PATH = os.path.join(TEST_UTIL_DIRECTORY, 'preptools_config.json')
TEST_WRONG_CONFIG_PATH = os.path.join(TEST_UTIL_DIRECTORY, 'wrong_preptools_config.json')
TEST_KEYSTORE_PATH = os.path.join(TEST_UTIL_DIRECTORY, 'test_keystore')
TEST_KEYSTORE_PASSWORD = 'qwer1234%'
TEST_REGISTER_JSON_PATH = os.path.join(TEST_UTIL_DIRECTORY, 'registerPRep.json')
TEST_SET_JSON_PATH = os.path.join(TEST_UTIL_DIRECTORY, 'setPRep.json')

REGISTER_SAMPLE = {
    "jsonrpc": "2.0",
    "method": "icx_sendTransaction",
    "id": 1234,
    "params": {
        "version": "0x3",
        "from": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
        "to": "cx0000000000000000000000000000000000000000",
        "stepLimit": "0x10000000",
        "timestamp": "0x58f962d10ff4e",
        "nid": "0x3",
        "value": "0x6c6b935b8bbd400000",
        "dataType": "call",
        "data": {
            "method": "registerPRep",
            "params": {
                "name": "banana node",
                "country": "KOR",
                "city": "Seoul",
                "email": "banana@example.com",
                "website": "https://icon.banana.com",
                "details": "https://icon.banana.com/json",
                "p2pEndpoint": "node.example.com:7100",
                "nodeAddress": "hx1234567890123456789012345678901234567890"
            }
        },
        "signature": "nJpIQckwQFsoOjlGtfLde1JyWtfho0bIucsa8yGbsyp3IxWcERCiNAah1Npjco0DH6htB/zFvBEi2ITMPvt3NwA="
    }
}


SET_SAMPLE = {
    "jsonrpc": "2.0",
    "method": "icx_sendTransaction",
    "id": 1234,
    "params": {
        "version": "0x3",
        "from": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
        "to": "cx0000000000000000000000000000000000000000",
        "stepLimit": "0x10000000",
        "timestamp": "0x58f9665c32947",
        "nid": "0x3",
        "value": "0x0",
        "dataType": "call",
        "data": {
            "method": "setPRep",
            "params": {
                "name": "kokoa node",
                "country": "KOR",
                "website": "https://icon.kokoa.com",
                "details": "https://icon.kokoa.com/json",
                "p2pEndpoint": "node.example.com:7100"
            }
        },
        "signature": "Yp1sSvRp4qEA7VtXQeY5mxXi1PXT5Ep3acB+AcwESBZCJMaMrwBA5fXIIKXDH257asEcgFNiq1zn24LEgJRXegE="
    }
}

UNREGISTER_SAMPLE = {
    "jsonrpc": "2.0",
    "method": "icx_sendTransaction",
    "id": 1234,
    "params": {
        "version": "0x3",
        "from": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
        "to": "cx0000000000000000000000000000000000000000",
        "stepLimit": "0x10000000",
        "timestamp": "0x58f96635f8cb1",
        "nid": "0x3",
        "value": "0x0",
        "dataType": "call",
        "data": {
            "method": "unregisterPRep"
        },
        "signature": "5nrgXNw2mxlbkYwpaR/5XzFQKK/PwTymELmlhTnKcDIVbQEsL59o0KPjEiEwavJE/XohF/TYTXxJLh16O0da0QA="
    }
}

SET_BONDER_LIST_SAMPLE = {
    "jsonrpc": "2.0",
    "method": "icx_sendTransaction",
    "id": 1234,
    "params": {
        "version": "0x3",
        "from": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
        "to": "cx0000000000000000000000000000000000000000",
        "stepLimit": "0x10000000",
        "timestamp": "0x58f966811dde2",
        "nid": "0x3",
        "value": "0x0",
        "dataType": "call",
        "data": {
            "method": "setBonderList",
            "params": {
                "bonderList": [
                    "hx0000000000000000000000000000000000000001",
                    "hx0000000000000000000000000000000000000002",
                    "hx0000000000000000000000000000000000000003",
                    "hx0000000000000000000000000000000000000004",
                    "hx0000000000000000000000000000000000000005",
                    "hx0000000000000000000000000000000000000006",
                    "hx0000000000000000000000000000000000000007",
                    "hx0000000000000000000000000000000000000008",
                    "hx0000000000000000000000000000000000000009",
                    "hx000000000000000000000000000000000000000a",
                ]
            }
        },
        "signature": "eY1hw7cfTIDxb5EV5En+uL2MT2BOagHt527nzIoC20QxQo8nCquwUGLbsDBTNBwuoq4UZmf7EDcMwJxSULzbNQA="
    }
}


GET_BONDER_LIST_SAMPLE = {
    "jsonrpc": "2.0",
    "method": "icx_call",
    "id": 1234,
    "params": {
        "to": "cx0000000000000000000000000000000000000000",
        "dataType": "call",
        "data": {
            "method": "getBonderList",
            "params": {
                "address": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6"
            }
        },
        "from": "hx1234567890123456789012345678901234567890"
    }
}


GET_PREP_SAMPLE = {
    "jsonrpc": "2.0",
    "method": "icx_call",
    "id": 1234,
    "params": {
        "to": "cx0000000000000000000000000000000000000000",
        "dataType": "call",
        "data": {
            "method": "getPRep",
            "params": {
                "address": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6"
            }
        },
        "from": "hx1234567890123456789012345678901234567890"
    }
}


GET_PREPS_SAMPLE = {
    "jsonrpc": "2.0",
    "method": "icx_call",
    "id": 1234,
    "params": {
        "to": "cx0000000000000000000000000000000000000000",
        "dataType": "call",
        "data": {
            "method": "getPReps"
        },
        "from": "hx1234567890123456789012345678901234567890"
    }
}


GET_TRANSACTION_RESULT_SAMPLE = {
    "jsonrpc": "2.0",
    "method": "icx_getTransactionResult",
    "id": 1234,
    "params": {
        "txHash": "0x001d8d2b99c0169df7f7545168451a2fb0608cc218e74ecec15516bf836bcd39"
    }
}


GET_TRANSACTION_SAMPLE = {
    "jsonrpc": "2.0",
    "method": "icx_getTransactionByHash",
    "id": 1234,
    "params": {
        "txHash": "0x1a4809d0a0446da469361e63a36265238f1dec6ff1afa10383231a64ed650692"
    }
}