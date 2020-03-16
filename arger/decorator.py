from argparse import ArgumentParser
from typing import Any, Callable, Dict, TypeVar, Optional

from .parser import opterate

CMD = "commands"
F = TypeVar('F', bound=Callable[..., Any])


class Arger:
    """A decorator to ease up the process of creating parser

    Examples
        in a file called main.py
        ``
        from arger import Arger
        arger = Arger("cli tool's title")

        @arger
        def build(remove=False):
            '''
            Args:
                remove: --rm -r you can specify the short option in the docstring
            '''
            print(remove)

        @arger
        def install(code:int):
            assert type(code) == int
            build()

        if __name__ == "__main__":
            arger.dispatch()
        ``

        -- run this with

        python main.py build --rm
        python main.py install 10
    """

    def __init__(self, desc: Optional[str] = None, add_help=True):
        self.desc = desc
        self.add_help = add_help
        self.funcs = {} # type: Dict[str, Any]

    @property
    def first_func(self):
        return self.funcs[list(self.funcs)[0]]

    def get_parser(self) -> ArgumentParser:
        if len(self.funcs) == 1:
            parser = opterate(self.first_func)
        else:
            parser = ArgumentParser(description=self.desc, add_help=self.add_help)
            commands = parser.add_subparsers(help=CMD)
            for func in self.funcs:
                opterate(func, commands)

        return parser

    def dispatch(self, *args):
        if not self.funcs:
            raise NotImplementedError("No function added.")

        parser = self.get_parser()
        args = vars(parser.parse_args(args))
        if len(self.funcs) == 1:
            return self.first_func(**args)

        func = self.funcs[args[CMD]]
        return func(**args)

    def __call__(self, func: F) -> F:
        """Decorator.

        called as a decorator to add any function as a command to the parser
        """
        self.funcs[func.__name__] = func
        return func
