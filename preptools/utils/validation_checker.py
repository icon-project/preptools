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

import re

import iso3166

from preptools.exception import InvalidFormatException, InvalidDataTypeException, InvalidArgumentException
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
        raise InvalidArgumentException("Type 0 have to has 'value' value.")

    return True


def valid_proposal_reivision_update_param(args) -> bool:

    if args.value_code is None or args.value_name is None:
        raise InvalidArgumentException("Type 1 have to has 'code' and 'name' value.")

    return True


def valid_proposal_malicious_score_param(args) -> bool:

    if args.value_address is None or args.value_type is None:
        raise InvalidArgumentException("Type 2 have to has 'address' and 'type' value.")

    return True


def valid_proposal_prep_disqualification_param(args) -> bool:

    if args.value_address is None:
        raise InvalidArgumentException("Type 3 have to has 'address' value.")

    return True


def valid_proposal_step_price(args) -> bool:

    if args.value_value is None:
        raise InvalidArgumentException("Type 4 have to has 'value' value.")

    try:
        int(args.value_value)
    except Exception:
        raise InvalidDataTypeException("value's type should be integer")

    return True


valid_proposal_param_by_type = [
    valid_proposal_text_param,                      # type 0
    valid_proposal_reivision_update_param,          # type 1
    valid_proposal_malicious_score_param,           # type 2
    valid_proposal_prep_disqualification_param,     # type 3
    valid_proposal_step_price                       # type 4
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
