import re

from prep.prep_exception import PrepStringFormatException


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

    raise PrepStringFormatException(f"There's no key named '{key}'")


def check_email_format(email: str) -> str:
    email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    if email_pattern.match(email) is None:
        raise PrepStringFormatException("invalid Email")

    return email


def check_name_format(name: str) -> str:
    name_pattern = re.compile(r"(^[a-zA-Z' ']+$)")

    if name_pattern.match(name) is None:
        raise PrepStringFormatException("invalid Name")

    return name


def check_city_format(city: str) -> str:
    city_pattern = re.compile(r"(^[a-zA-Z' ']+$)")

    if city_pattern.match(city) is None:
        raise PrepStringFormatException("invalid city")

    return city


def check_country_format(country: str) -> str:
    country_pattern = re.compile(r"(^[A-Z]{3}$)")

    if country_pattern.match(country) is None:
        raise PrepStringFormatException("invalid country")

    return country


def check_website_format(website: str) -> str:
    if not _is_valid_website(website):
        raise PrepStringFormatException("invalid website")

    return website


def check_details_format(details: str) -> str:
    if not _is_valid_details(details):
        raise PrepStringFormatException("invalid details")

    return details


def check_p2p_endpoint_format(p2p_endpoint: str) -> str:
    if not _is_valid_p2p_endpoint(p2p_endpoint):
        raise PrepStringFormatException("invalid p2pEndpoint")

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
