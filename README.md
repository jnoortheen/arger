# Overview

A wrapper around argparser to help build CLIs from functions. Uses type-hints extensively :snake:.

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

or add it to your [Poetry](https://poetry.eustace.io/) project:

``` text
$ poetry add arger
```

# :books: Usage

* create a python file called test.py

``` python
from arger import Arger

def main(param1: int, param2: str, kw1=None, kw2=False):
    """Example function with types documented in the docstring.

    :param param1: The first parameter.
    :param param2: The second parameter.
    """
    print(locals())

if __name__ == '__main__':
    Arger(main).run()
```

* Here Arger is just a subclass of `ArgumentParser`. It will not conceal you from using other `argparse` libraries.

* run this normally with

``` sh
python test.py 100 param2
```

* Checkout [examples](docs/examples) folder and documentation to see more of `arger` in action. It supports any level of sub-commands.

# Features

- Uses docstring to parse help comment for arguments. Supports
    + [google](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
    + [numpy](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy)
    + [rst](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- Flags will be generated from parameter-name. 
  If needed you could declare it inside docstring like `:param arg1: -a --arg this is the document`.
  Also one can use `def main(arg1:int=Argument(flags=('-a', '--arg'), ...): ...`
- The decorated functions can be composed to form nested sub-commands of any level.
- No external lib dependency
- Most of the Standard types [supported](./tests/test_args_opts/test_arguments.py). 
  Please see [examples](./docs/examples/4-supported-types/src.py) for more supported types with examples.
- All argument to `ArgumentParser.add_argument` is supported. 
  It can be updated with `arger.Argument` classes.
- `*args` supported but no `**kwargs` support yet.
- all optional arguments that start with underscore is not passed to `Parser`. 
  They are considered private to the function implementation.
  Some parameter names with special meaning
    - `_namespace_` -> to get the output from the `ArgumentParser.parse_args()`
    - `_arger_` -> to get the parser instance
  

This project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).


# Argparser enhancements

* web-ui : https://github.com/nirizr/argparseweb
* extra actions : https://github.com/kadimisetty/action-hero
* automatic shell completions using [argcomplete](https://github.com/kislyuk/argcomplete)
