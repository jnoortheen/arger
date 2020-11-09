from pkg_resources import DistributionNotFound, get_distribution

from .main import Arger, Argument, Option

try:
    __version__ = get_distribution("arger").version
except DistributionNotFound:
    __version__ = "(local)"

__all__ = ["Arger", "Argument", "Option"]
