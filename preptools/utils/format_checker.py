import re

from preptools.exception import PRepToolsStringFormatException


def check_prep(prep: dict) -> dict:

    for k, v in prep.items():
        check_prep_by_key(k, v)

    return prep


def check_prep_by_key(key: str, value: str) -> str:

    if key == 'name':
        return check_name_format(value)
    elif key == 'email':
        return check_email_format(value)
    elif key == 'city':
        return check_city_format(value)
    elif key == 'country':
        return check_country_format(value)
    elif key == 'website':
        return check_website_format(value)
    elif key == 'details':
        return check_details_format(value)
    elif key == 'p2pEndpoint':
        return check_p2p_endpoint_format(value)

    raise PRepToolsStringFormatException(f"There's no key named '{key}'")


def check_email_format(email: str, is_blank_able: bool = False) -> str:
    if is_blank_able and email == '':
        return email

    email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    if email_pattern.match(email) is None:
        raise PRepToolsStringFormatException("invalid Email")

    return email


def check_name_format(name: str, is_blank_able: bool = False) -> str:
    if is_blank_able and name == '':
        return name

    name_pattern = re.compile(r"(^[a-zA-Z' ']+$)")

    if name_pattern.match(name) is None:
        raise PRepToolsStringFormatException("invalid Name")

    return name


def check_city_format(city: str, is_blank_able: bool = False) -> str:
    if is_blank_able and city == '':
        return city

    city_pattern = re.compile(r"(^[a-zA-Z' ']+$)")

    if city_pattern.match(city) is None:
        raise PRepToolsStringFormatException("invalid city")

    return city


def check_country_format(country: str, is_blank_able: bool = False) -> str:
    if is_blank_able and country == '':
        return country

    country_pattern = re.compile(r"(^[A-Z]{3}$)")

    if country_pattern.match(country) is None:
        raise PRepToolsStringFormatException("invalid country")

    return country


def check_website_format(website: str, is_blank_able: bool = False) -> str:
    if is_blank_able and website == '':
        return website

    if not _is_valid_website(website):
        raise PRepToolsStringFormatException("invalid website")

    return website


def check_details_format(details: str, is_blank_able: bool = False) -> str:
    if is_blank_able and details == '':
        return details

    if not _is_valid_details(details):
        raise PRepToolsStringFormatException("invalid details")

    return details


def check_p2p_endpoint_format(p2p_endpoint: str, is_blank_able: bool = False) -> str:
    if is_blank_able and p2p_endpoint == '':
        return p2p_endpoint

    if not _is_valid_p2p_endpoint(p2p_endpoint):
        raise PRepToolsStringFormatException("invalid p2pEndpoint")

    return p2p_endpoint


def _is_valid_website(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?/?$', re.IGNORECASE)

    return url is not None and regex.search(url)


def _is_valid_details(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return url is not None and regex.search(url)


def _is_valid_p2p_endpoint(p2p_endpoint):
    regex = re.compile(
        r'(^(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?$', re.IGNORECASE)

    return p2p_endpoint is not None and regex.search(p2p_endpoint)
