import pkg_resources

__version__ = "1.3.2"


def get_version() -> str:
    try:
        version = pkg_resources.get_distribution('preptools').version
    except pkg_resources.DistributionNotFound:
        version = __version__
    return version
