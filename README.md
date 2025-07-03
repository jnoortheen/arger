# Overview

A wrapper around stdlib [argparse](https://docs.python.org/3/library/argparse.html) to help build CLIs from functions using type-hints :snake:.

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

* create a python file called test.py

``` py
from arger import Arger


def main(param1: int, param2: str, kw1=None, kw2=False):
    """Example function with types documented in the docstring.

    Args:
        param1: The first parameter.
        param2: The second parameter.
        kw1: this is optional parameter.
        kw2: this is boolean. setting flag sets True.
    """
    print(locals())


arger = Arger(
    main,
    prog="pytest",  # for testing purpose. otherwise not required
)

if __name__ == "__main__":
    arger.run()
```

* Here Arger is just a subclass of `ArgumentParser`. It will not conceal you from using other `argparse` libraries.

* run this normally with

```sh
$ python test.py -h
usage: pytest [-h] [-k KW1] [-w] param1 param2

Example function with types documented in the docstring.

positional arguments:
  param1             The first parameter.
  param2             The second parameter.

optional arguments:
  -h, --help         show this help message and exit
  -k KW1, --kw1 KW1  this is optional parameter. (default: None)
  -w, --kw2          this is boolean. setting flag sets True. (default: False)
```

``` sh
$ python test.py 100 param2
{'param1': 100, 'param2': 'param2', 'kw1': None, 'kw2': False}
```

* Checkout [examples](docs/examples) folder and documentation to see more of `arger` in action. It supports any level of sub-commands.

# Features

- Uses docstring to parse help comment for arguments. Supports
    + [google](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
    + [numpy](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy)
    + [rst](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- Flags will be generated from parameter-name.
  1.  e.g. `def main(param: ...)` -> `-p, --param`
  2.  If needed you could declare it inside docstring like `:param arg1: -a --arg this is the document`.
- one can use `Argument` class to pass any values to the
  [parser.add_argument](https://docs.python.org/3/library/argparse.html#the-add-argument-method) function
- The decorated functions can be composed to form nested sub-commands of any level.
- Most of the Standard types [supported](./tests/test_args_opts/test_arguments.py).
  Please see [examples](./docs/examples/4-supported-types/src.py) for more supported types with examples.
- No external dependency other than stdlib.

> **_NOTE_**
>  - `*args` supported but no `**kwargs` support yet.
>  - all optional arguments that start with underscore is not passed to `Parser`.
>    They are considered private to the function implementation.
>    Some parameter names with special meaning
>      - `_namespace_` -> to get the output from the `ArgumentParser.parse_args()`
>      - `_arger_` -> to get the parser instance

# Argparser enhancements

* web-ui : https://github.com/nirizr/argparseweb
* extra actions : https://github.com/kadimisetty/action-hero
* automatic shell completions using [argcomplete](https://github.com/kislyuk/argcomplete)
