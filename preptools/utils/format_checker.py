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

from preptools.preptools_exception import InvalidFormatException
from ..base.type_converter_templates import ConstantKeys

scheme_pattern = r'^(http:\/\/|https:\/\/)'
path_pattern = r'(\/\S*)?$'
port_regex = r'(:[0-9]{1,5})?'
ip_regex = r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
host_name_regex = r'(localhost|(?:[\w\d](?:[\w\d-]{0,61}[\w\d])\.)+[\w\d][\w\d-]{0,61}[\w\d])'
email_regex = r'^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*@' + host_name_regex + '$'
ENDPOINT_DOMAIN_NAME_PATTERN = re.compile(f'^{host_name_regex}{port_regex}$')
ENDPOINT_IP_PATTERN = re.compile(f'^{ip_regex}{port_regex}$')
WEBSITE_DOMAIN_NAME_PATTERN = re.compile(f'{scheme_pattern}{host_name_regex}{port_regex}{path_pattern}$')
WEBSITE_IP_PATTERN = re.compile(f'{scheme_pattern}{ip_regex}{port_regex}{path_pattern}$')
EMAIL_PATTERN = re.compile(email_regex)


def validate_prep_data(data: dict, set_prep: bool = False):
    if not set_prep:
        fields_to_validate = (
            ConstantKeys.NAME,
            ConstantKeys.COUNTRY,
            ConstantKeys.CITY,
            ConstantKeys.EMAIL,
            ConstantKeys.WEBSITE,
            ConstantKeys.DETAILS,
            ConstantKeys.P2P_ENDPOINT
        )

        for key in fields_to_validate:
            if key not in data:
                raise InvalidFormatException(f'"{key}" not found')
            elif len(data[key].strip()) < 1:
                raise InvalidFormatException("Can not set empty data")

    for key in data:
        if set_prep:
            if len(data[key].strip()) == 0:
                continue
        if len(data[key].strip()) < 1:
            raise InvalidFormatException("Can not set empty data")
        if key == ConstantKeys.P2P_ENDPOINT:
            _validate_p2p_endpoint(data[key])
        elif key in (ConstantKeys.WEBSITE, ConstantKeys.DETAILS):
            _validate_uri(data[key])
        elif key == ConstantKeys.EMAIL:
            _validate_email(data[key])
        elif key == ConstantKeys.COUNTRY:
            _validate_country(data[key])


def _validate_p2p_endpoint(p2p_endpoint: str):
    network_locate_info = p2p_endpoint.split(":")

    if len(network_locate_info) != 2:
        raise InvalidFormatException("Invalid endpoint format. endpoint must have port info")

    _validate_port(network_locate_info[1], ConstantKeys.P2P_ENDPOINT)

    if ENDPOINT_IP_PATTERN.match(p2p_endpoint):
        return

    if not ENDPOINT_DOMAIN_NAME_PATTERN.match(p2p_endpoint.lower()):
        raise InvalidFormatException("Invalid endpoint format")


def _validate_uri(uri: str):
    uri = uri.lower()
    if WEBSITE_DOMAIN_NAME_PATTERN.match(uri):
        return
    if WEBSITE_IP_PATTERN.match(uri):
        return

    raise InvalidFormatException("Invalid uri format")


def _validate_port(port: str, validating_field: str):
    try:
        port = int(port, 10)
    except ValueError:
        raise InvalidFormatException(f'Invalid {validating_field} format. port: "{port}"')

    if not 0 < port < 65536:
        raise InvalidFormatException(f"Invalid {validating_field} format. Port out of range: {port}")


def _validate_email(email: str):
    if not EMAIL_PATTERN.match(email):
        raise InvalidFormatException("Invalid email format")


def _validate_country(country_code: str):
    if country_code.upper() not in iso3166.countries_by_alpha3:
        raise InvalidFormatException("Invalid alpha-3 country code")