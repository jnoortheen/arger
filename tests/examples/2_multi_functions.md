# Usages

1. ran help
```shell script
$ python 2_multi_functions.py -h
usage: pytest [-h] {create,remove,list} ...

App Description goes here

optional arguments:
  -h, --help            show this help message and exit

commands:
  {create,remove,list}
    create              Create new test.
    remove              Remove a test with variadic argument.
    list                List all tests.
```

1. ran create help
```shell script
$ python 2_multi_functions.py create -h
usage: pytest create [-h] name

positional arguments:
  name        Name of the test

optional arguments:
  -h, --help  show this help message and exit
```

1. ran remove help
```shell script
$ python 2_multi_functions.py remove -h
usage: pytest remove [-h] [name [name ...]]

positional arguments:
  name        tests to remove

optional arguments:
  -h, --help  show this help message and exit
```

1. ran list help
```shell script
$ python 2_multi_functions.py list -h
usage: pytest list [-h]

optional arguments:
  -h, --help  show this help message and exit
```


1. ran create
```shell script
$ python 2_multi_functions.py create direcory
name (<class 'str'>): direcory
```


1. ran remove
```shell script
$ python 2_multi_functions.py remove direcory
name (<class 'tuple'>): ('direcory',)
```


1. ran list
```shell script
$ python 2_multi_functions.py list
container (<class 'list'>): []
```

1. ran combined
```shell script
$ python 2_multi_functions.py create directory list
usage: pytest [-h] {create,remove,list} ...
pytest: error: unrecognized arguments: list
```
