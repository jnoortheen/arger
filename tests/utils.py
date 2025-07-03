from argparse import Namespace

from arger.main import FUNC_PREFIX


def _reprint(**kwargs):
    for param, value in sorted(kwargs.items()):
        if isinstance(value, Namespace):
            val = sorted([(k, (v.__name__ if k.startswith(FUNC_PREFIX) else v)) for k, v in vars(value).items()])
        else:
            val = value
        print(f"{param} ({type(value)}): {val}")
