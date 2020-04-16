import argparse


# create the top-level parser
parser = argparse.ArgumentParser(prog="PROG", description="parser desc")
parser.add_argument("--foo", action="store_true", help="foo help")
subparsers = parser.add_subparsers(
    title="Commands",
    dest="command"
    # help='sub-command help'
)

# create the parser for the "a" command
parser_a = subparsers.add_parser("a", help="a help")
parser_a.add_argument("bar", type=int, help="bar help")
# create the parser for the "b" command
parser_b = subparsers.add_parser("b", help="b help")
parser_b.add_argument("--baz", choices="XYZ", help="baz help")


def doc():
    """
    # parse some argument lists
    >>> parser.parse_args(['a', '12'])
    Namespace(bar=12, foo=False)
    >>> parser.parse_args(['--foo', 'b', '--baz', 'Z'])
    Namespace(baz='Z', foo=True)
    >>> parser.parse_args(['b', '--baz', 'Z',])
    Namespace(baz='Z', foo=False)
    """


if __name__ == "__main__":
    parser.parse_args(["-h"])
