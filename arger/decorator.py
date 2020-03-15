from argparse import ArgumentParser
from types import FunctionType
from typing import Dict

from .parser import opterate


CMD = "commands"


class Arger:
    def __init__(self, desc: str, add_help=True):
        self.parser = ArgumentParser(description=desc, add_help=add_help)
        self.commands = self.parser.add_subparsers(CMD)
        self.funcs = {}  # type: Dict[str, FunctionType]

    def dispatch(self, *args):
        args = vars(self.parser.parse_args(args))
        func = self.funcs[args[CMD]]
        return func(**args)

    def __call__(self, func: FunctionType):
        """Decorator.

        called as a decorator to add any function as a command to the parser
        """
        self.funcs[func.__name__] = func
        opterate(self.commands, func)
