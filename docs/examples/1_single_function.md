# Single Command
in a file named `main.py`

```python
--8<-- "single_function.py"
```

## ran with both positional arguments

```sh
$ python single_function.py 10 p2
kw1 (<class 'NoneType'>): None
kw2 (<class 'bool'>): False
param1 (<class 'int'>): 10
param2 (<class 'str'>): p2
```

##  ran empty
```sh
$ python single_function.py
usage: pytest [-h] [-k KW1] [-w] param1 param2
pytest: error: the following arguments are required: param1, param2
```

## ran help
```sh
$ python single_function.py --help
usage: pytest [-h] [-k KW1] [-w] param1 param2

Example function with types documented in the docstring.

positional arguments:
  param1             The first parameter.
  param2             The second parameter.

optional arguments:
  -h, --help         show this help message and exit
  -k KW1, --kw1 KW1
  -w, --kw2
```

## ran with invalid option
```sh
$ python single_function.py --invalid
usage: pytest [-h] [-k KW1] [-w] param1 param2
pytest: error: the following arguments are required: param1, param2
```

## ran with invalid type
```sh
$ python single_function.py p1 p2
usage: pytest [-h] [-k KW1] [-w] param1 param2
pytest: error: argument param1: invalid int value: 'p1'
```

## ran with one argument missing
```sh
$ python single_function.py p1
usage: pytest [-h] [-k KW1] [-w] param1 param2
pytest: error: argument param1: invalid int value: 'p1'
```
