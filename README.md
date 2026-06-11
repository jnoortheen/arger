# Overview

A lightweight wrapper around [argparse](https://docs.python.org/3/library/argparse.html) to help build CLIs from functions.

[![PyPi Version](https://img.shields.io/pypi/v/arger.svg?style=flat)](https://pypi.python.org/pypi/arger)
[![Python Version](https://img.shields.io/pypi/pyversions/arger.svg)](https://pypi.org/project/arger/)
![](https://github.com/jnoortheen/arger/workflows/test-and-publish/badge.svg)
![](https://github.com/jnoortheen/arger/workflows/codeql-analysis/badge.svg)
![](https://img.shields.io/badge/dynamic/json?label=coverage&query=%24.coverage.status&url=https%3A%2F%2Fraw.githubusercontent.com%2Fjnoortheen%2Farger%2Fshields%2Fshields.json)
[![PyPI License](https://img.shields.io/pypi/l/arger.svg)](https://pypi.org/project/arger)

# Setup

## :gear: Installation

Install it directly into an activated virtual environment:

``` text
$ pip install arger
```

# :books: Usage

* Create a Python file called `test.py`:

``` py
from arger import Arger


def main(param1: int, param2: str, kw1=None, kw2=False):
    """Example function with types documented in the docstring.

    Args:
        param1: The first parameter.
        param2: The second parameter.
        kw1: This is an optional parameter.
        kw2: This is a boolean. Setting the flag sets it to True.
    """
    print(locals())


arger = Arger(
    main,
    prog="pytest",  # for testing purposes; otherwise, not required
)

if __name__ == "__main__":
    arger.run()
```

* Here `Arger` is just a subclass of `ArgumentParser`. It does not prevent you from using standard `argparse` features.

* Run this normally with:

```sh
$ python test.py -h
usage: pytest [-h] [-k KW1] [-w] param1 param2

Example function with types documented in the docstring.

positional arguments:
  param1             The first parameter.
  param2             The second parameter.

optional arguments:
  -h, --help         show this help message and exit
  -k KW1, --kw1 KW1  This is an optional parameter. (default: None)
  -w, --kw2          This is a boolean. Setting the flag sets it to True. (default: False)
```

``` sh
$ python test.py 100 param2
{'param1': 100, 'param2': 'param2', 'kw1': None, 'kw2': False}
```

* Check out the [examples](docs/examples) folder and documentation to see more of `arger` in action. It supports any level of sub-commands.

# Features

- Uses the docstring to parse help descriptions for arguments. Supports:
    + [google](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
    + [numpy](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy)
    + [rst](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- Flags will be generated from parameter names.
  1.  E.g., `def main(param: ...)` -> `-p, --param`
  2.  If needed, you can declare them inside the docstring, like `:param arg1: -a --arg this is the document`.
- One can use the `Argument` class to pass any values to the
  [parser.add_argument](https://docs.python.org/3/library/argparse.html#the-add-argument-method) function.
- The decorated functions can be composed to form nested sub-commands of any level.
- Most standard types are [supported](./tests/test_args_opts/test_arguments.py).
  Please see the [examples](./docs/examples/4-supported-types/src.py) for more supported types with code examples.
- No external dependency other than the standard library.

> **_NOTE_**
>  - `*args` is supported, but there is no `**kwargs` support yet.
>  - Any optional argument starting with an underscore is not passed to the parser.
>    They are considered private to the function's implementation.
>    Some parameter names have special meaning:
>      - `_namespace_` -> gets the output from `ArgumentParser.parse_args()`
>      - `_arger_` -> gets the parser instance

# Argparser enhancements

* web-ui : https://github.com/nirizr/argparseweb
* extra actions : https://github.com/kadimisetty/action-hero
* automatic shell completions using [argcomplete](https://github.com/kislyuk/argcomplete)
