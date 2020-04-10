# Usages
1. ran empty
```shell script
$ python 1_single_function.py
usage: pytest [-h] [-k KW1] [-w] param1 param2
pytest: error: the following arguments are required: param1, param2
```

2. ran help
```shell script
$ python 1_single_function.py
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

3. ran with invalid option
```shell script
$ python 1_single_function.py --invalid
usage: pytest [-h] [-k KW1] [-w] param1 param2
pytest: error: the following arguments are required: param1, param2
```

4. ran with one argument missing
```shell script
$ python 1_single_function.py p1
usage: pytest [-h] [-k KW1] [-w] param1 param2
pytest: error: the following arguments are required: param2
```

5. ran with both options
```shell script
$ python 1_single_function.py 10 p2
```
