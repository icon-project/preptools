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

from preptools.exception import InvalidFormatException
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

    if key == ConstantKeys.P2P_ENDPOINT:
        validate_p2p_endpoint(value)
    elif key in (ConstantKeys.WEBSITE, ConstantKeys.DETAILS):
        validate_uri(value)
    elif key == ConstantKeys.EMAIL:
        validate_email(value)
    elif key == ConstantKeys.COUNTRY:
        validate_country(value)


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
