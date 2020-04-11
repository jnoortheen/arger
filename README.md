# Overview

A wrapper around argparser to help build CLIs from functions. Uses typehints extensively.

[![PyPi Version](https://img.shields.io/pypi/v/arger.svg?style=flat)](https://pypi.python.org/pypi/arger)
[![Python Version](https://img.shields.io/pypi/pyversions/returns.svg)](https://pypi.org/project/arger/)

[![Unix Build Status](https://img.shields.io/travis/jnoortheen/arger/master.svg?label=unix)](https://travis-ci.org/jnoortheen/arger)
[![Windows Build Status](https://img.shields.io/appveyor/ci/jnoortheen/arger/master.svg?label=windows)](https://ci.appveyor.com/project/jnoortheen/arger)
[![Coverage Status](https://img.shields.io/coveralls/jnoortheen/arger/master.svg)](https://coveralls.io/r/jnoortheen/arger)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/jnoortheen/arger.svg)](https://scrutinizer-ci.com/g/jnoortheen/arger/?branch=master)
[![PyPI Version](https://img.shields.io/pypi/v/arger.svg)](https://pypi.org/project/arger)
[![PyPI License](https://img.shields.io/pypi/l/arger.svg)](https://pypi.org/project/arger)

# Setup

## Installation

Install it directly into an activated virtual environment:

```text
$ pip install arger
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```text
$ poetry add arger
```

# Usage
- create a python file called test.py
```python
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

- run this normally with 

```shell script
$ python test.py 100 param2
```

- Checkout [examples](./tests/examples) folder and documentation to see more of `arger` in action.

# Alternatives

## [argh](https://argh.readthedocs.io/en/latest/tutorial.html) 
 - has similar goals as to ease up using argparser. 
 - doesn't support type hints. 
 - No recent releases.

## [typer](https://github.com/tiangolo/typer)
 - if you are using `click`, I highly recommend you to check this library.
 - it is neat and many features are inspired from this library.
 - doesn't support loading help text for arguments from docstrings.
 
## [invoke](http://www.pyinvoke.org/) 
 - doesn't support type hints.

## [cliche](https://github.com/kootenpv/cliche)
 - has similar goals. 
 - doesn't cover much use cases as `arger`.

This project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).
