from argparse import Namespace


def _reprint(**kwargs):
    for param, value in sorted(kwargs.items()):
        if isinstance(value, Namespace):
            val = sorted(vars(value).items())
        else:
            val = value
        print(f"{param} ({type(value)}): {val}")
