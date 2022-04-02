# -*- coding: utf-8 -*-
# Copyright 2019 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import re

import iso3166
import requests

from preptools.exception import InvalidFormatException, JsonRpcException, InvalidArgumentException
from preptools.utils.constants import fields_to_validate, ConstantKeys

scheme_pattern = r'^(http:\/\/|https:\/\/)'
path_pattern = r'(\/\S*)?$'
port_regex = r'(:[0-9]{1,5})?'
ip_regex = r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
host_name_regex = r'(localhost|(?:[\w\d](?:[\w\d-]{0,61}[\w\d])\.)+[\w\d][\w\d-]{0,61}[\w\d])'
email_regex = r'^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*@' + host_name_regex + '$'
password_regex = r'^(?=.*\d)(?=.*[a-zA-Z])(?=.*[?!:\.,%+-/*<>{}\(\)\[\]`"\'~_^\\|@#$&]).{8,}$'
ENDPOINT_DOMAIN_NAME_PATTERN = re.compile(f'^{host_name_regex}{port_regex}$')
ENDPOINT_IP_PATTERN = re.compile(f'^{ip_regex}{port_regex}$')
WEBSITE_DOMAIN_NAME_PATTERN = re.compile(f'{scheme_pattern}{host_name_regex}{port_regex}{path_pattern}$')
WEBSITE_IP_PATTERN = re.compile(f'{scheme_pattern}{ip_regex}{port_regex}{path_pattern}$')
EMAIL_PATTERN = re.compile(email_regex)
PASSWORD_PATTERN = re.compile(password_regex)
CHAINSCORE_ADDRESS = f"cx{'0' * 40}"


def validate_prep_data(data: dict, blank_able: bool = False):
    if not blank_able:

        for key in fields_to_validate:
            if key not in data:
                raise InvalidFormatException(f'"{key}" not found')
            elif len(data[key].strip()) < 1:
                raise InvalidFormatException("Can not set empty data")

    for key in data:
        if len(data[key].strip()) < 1 and not blank_able:
            raise InvalidFormatException("Can not set empty data")

        validate_field_in_prep_data(key, data[key])


def validate_field_in_prep_data(key: str, value: str):
    if not validate_field_key(key):
        raise InvalidFormatException(f"Invalid key : {key}")

    if key == ConstantKeys.P2P_ENDPOINT:
        validate_p2p_endpoint(value)
    elif key in (ConstantKeys.WEBSITE, ConstantKeys.DETAILS):
        validate_uri(value)
    elif key == ConstantKeys.EMAIL:
        validate_email(value)
    elif key == ConstantKeys.COUNTRY:
        validate_country(value)
    elif key == ConstantKeys.NODE_ADDRESS:
        validate_node_address(value)


def validate_field_key(key):
    for ckey in fields_to_validate:
        if key == ckey:
            return True

    return False


def validate_p2p_endpoint(p2p_endpoint: str):
    network_locate_info = p2p_endpoint.split(":")

    if len(network_locate_info) != 2:
        raise InvalidFormatException("Invalid endpoint format. endpoint must have port info")

    validate_port(network_locate_info[1], ConstantKeys.P2P_ENDPOINT)

    if ENDPOINT_IP_PATTERN.match(p2p_endpoint):
        return

    if not ENDPOINT_DOMAIN_NAME_PATTERN.match(p2p_endpoint.lower()):
        raise InvalidFormatException("Invalid endpoint format")


def validate_uri(uri: str):
    uri = uri.lower()
    if WEBSITE_DOMAIN_NAME_PATTERN.match(uri):
        return
    if WEBSITE_IP_PATTERN.match(uri):
        return

    raise InvalidFormatException("Invalid uri format")


def validate_port(port: str, validating_field: str):
    try:
        port = int(port, 10)
    except ValueError:
        raise InvalidFormatException(f'Invalid {validating_field} format. port: "{port}"')

    if not 0 < port < 65536:
        raise InvalidFormatException(f"Invalid {validating_field} format. Port out of range: {port}")


def validate_email(email: str):
    if not EMAIL_PATTERN.match(email):
        raise InvalidFormatException("Invalid email format")


def validate_country(country_code: str):
    if country_code.upper() not in iso3166.countries_by_alpha3:
        raise InvalidFormatException("Invalid alpha-3 country code")


def validate_password(password) -> bool:
    """Verify the entered password.

    :param password: The password the user entered. type(str)
    :return: bool
    True: When the password is valid format
    False: When the password is invalid format
    """

    return bool(PASSWORD_PATTERN.match(password))


def validate_node_address(address: str):
    if isinstance(address, str) and len(address) == 42:
        prefix, body = _split_icon_address(address)
        if prefix != 'hx' or not _is_lowercase_hex_string(body):
            raise InvalidFormatException("Invalid hx Address")
    else:
        raise InvalidFormatException("Invalid hx Address")


def valid_proposal_text_param(args) -> bool:
    if args.value_value is None:
        raise InvalidArgumentException("Type 0 must have 'value' value.")

    return True


def valid_revision_update_params(args) -> bool:
    if args.value_code is None or args.value_name is None:
        raise InvalidArgumentException("Type 1 must have 'code' and 'name' value.")

    return True


def validate_malicious_score_params(args) -> bool:
    if args.value_address is None or args.value_type is None:
        raise InvalidArgumentException("Type 2 must have 'address' and 'type' value.")

    return True


def validate_disqualification_param(args) -> bool:
    if args.value_address is None:
        raise InvalidArgumentException("Type 3 must have 'address' value.")

    return True


def is_value_integer(args) -> bool:
    if args.value_value is None:
        raise InvalidArgumentException("Type 4 and 5 must have 'value' value.")

    try:
        int(args.value_value)
    except Exception:
        raise InvalidArgumentException("value's type should be integer")

    return True


def is_iglobal_integer(args) -> bool:
    if args.value_iglobal is None:
        raise InvalidArgumentException("Type 7 must have 'iglobal' value.")

    try:
        int(args.value_iglobal)
    except Exception:
        raise InvalidArgumentException("iglobals's type should be integer")

    return True


def validate_step_costs_param(args) -> bool:
    if args.value_costs is None:
        raise InvalidArgumentException("Type 6 must have 'costs' value.")

    try:
        costs = args.value_costs
        value = {}
        for cost in costs:
            token = cost.split(",")
            value[token[0]] = hex(int(token[1], 0))
        args.value_costs = value
    except Exception:
        raise InvalidArgumentException("costs input is invalid. example) default,1234 get,10000")

    return True


def validate_reward_funds_allocation_params(args) -> bool:
    if args.value_rewardFunds is None:
        raise InvalidArgumentException("Type 8 must have 'rewardFunds' value.")

    try:
        reward_types = {"iprep", "icps", "irelay", "ivoter"}
        reward_funds = args.value_rewardFunds
        value = {}
        if len(reward_funds) != len(reward_types):
            print("rewardFunds must have 4 items. iprep, icps, irelay, ivoter")
            return False

        total = 0
        for reward_info in reward_funds:
            token = reward_info.split(",")
            key = token[0]
            ratio = int(token[1], 0)
            if key not in reward_types:
                print(f"{key} is invalid reward fund type")
                return False
            if ratio < 0:
                print("reward fund value must >= 0")
                return False
            value[key] = ratio
            total += ratio
            reward_types.remove(key)
        if total != 100:
            print("Sum of rewardFunds must be 100")
            return False
        args.value_rewardFunds = value
    except Exception:
        raise InvalidArgumentException("rewardFunds input is invalid. example) iprep,10 icps,20 irelay,30 ivoter,40")

    return True


valid_proposal_param_by_type = [
    valid_proposal_text_param,  # type 0
    valid_revision_update_params,  # type 1
    validate_malicious_score_params,  # type 2
    validate_disqualification_param,  # type 3
    is_value_integer,  # type 4
    is_value_integer,  # type 5
    validate_step_costs_param,  # type 6
    is_iglobal_integer,  # type 7
    validate_reward_funds_allocation_params,  # type 8
]


def _split_icon_address(address: str) -> (str, str):
    """Split icon address into 2-char prefix and 40-char address body

    :param address: 42-char address string
    :return: prefix, body
    """
    return address[:2], address[2:]


def _is_lowercase_hex_string(value: str) -> bool:
    """Check whether value is hexadecimal format or not

    :param value: text
    :return: True(lowercase hexadecimal) otherwise False
    """

    try:
        result = re.match('[0-9a-f]+', value)
        return len(result.group(0)) == len(value)
    except:
        pass

    return False


def check_enough_balance(url: str, data: dict) -> bool:
    address = data["from_"]
    value = data.get("value", 0)
    step_limit = data["step_limit"]
    balance_id, step_price_id = 1, 2
    balance_request = {
        'jsonrpc': '2.0',
        'method': "icx_getBalance",
        'id': balance_id,
        "params": {"address": address}
    }
    step_price_request = {
        'jsonrpc': '2.0',
        'method': "icx_call",
        'id': step_price_id,
        "params": {
            "to": CHAINSCORE_ADDRESS,
            "dataType": "call",
            "data": {
                "method": "getStepPrice"
            }
        }
    }
    batch_request = [balance_request, step_price_request]
    with requests.Session() as session:
        response = session.post(url=url, data=json.dumps(batch_request))
    if response.ok:
        balance_res, step_res = None, None
        res_list = response.json()
        for res in res_list:
            if res["id"] == balance_id:
                balance_res = res
            else:
                step_res = res
        balance = int(balance_res["result"], 0)
        step_price = int(step_res["result"], 0)
        if balance - (step_price * step_limit + value) > 0:
            return True
        else:
            print(f"Your balance({balance}) < cost(stepPrice * stepLimit + value): ({step_price * step_limit + value})")
            return False
    raise JsonRpcException("Error while checking balance")


def is_valid_address(address: str) -> bool:
    try:
        if not isinstance(address, str):
            return False
        if len(address) != 42:
            return False
        if address[:2] not in ("hx", "cx"):
            return False
        if not address.islower():
            return False

        _ = bytes.fromhex(address[2:])
        return True
    except:
        return False


def is_tx_hash(tx_hash: str) -> bool:
    try:
        if not isinstance(tx_hash, str):
            return False
        if not tx_hash.startswith("0x"):
            return False
        if not tx_hash.islower():
            return False
        return len(bytes.fromhex(tx_hash[2:])) == 32
    except:
        return False
