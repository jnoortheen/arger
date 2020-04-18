from pkg_resources import DistributionNotFound, get_distribution

from .arger import Arger
from .parser.classes import Argument, Option


try:
    __version__ = get_distribution("arger").version
except DistributionNotFound:
    __version__ = "(local)"

__all__ = [
    "Arger",
]
