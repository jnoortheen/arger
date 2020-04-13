# Usages

1. ran help
```shell script
$ python 3_nested_commands.py -h
usage: pytest [-h] [-v] [-l] [-o LOG_FILE] {create,remove,list} ...

App Description goes here.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         verbose output
  -l, --log
  -o LOG_FILE, --log_file LOG_FILE
                        name of the log file to write output

commands:
  {create,remove,list}
    create              Create new test.
    remove              Remove a test.
    list                List all tests.
```

1. ran create help
```shell script
$ python 3_nested_commands.py create -h
usage: pytest create [-h] name

positional arguments:
  name        Name of the test

optional arguments:
  -h, --help  show this help message and exit
```

1. ran remove help
```shell script
$ python 3_nested_commands.py remove -h
usage: pytest remove [-h] name

positional arguments:
  name        Name of the test

optional arguments:
  -h, --help  show this help message and exit
```

1. ran list help
```shell script
$ python 3_nested_commands.py list -h
usage: pytest list [-h]

optional arguments:
  -h, --help  show this help message and exit
```


1. ran create
```shell script
$ python 3_nested_commands.py create direcory
log (<class 'bool'>): False
log_file (<class 'NoneType'>): None
name (<class 'str'>): direcory
verbose (<class 'bool'>): False
```


1. ran remove
```shell script
$ python 3_nested_commands.py remove direcory
log (<class 'bool'>): False
log_file (<class 'NoneType'>): None
name (<class 'str'>): direcory
verbose (<class 'bool'>): False
```


1. ran list
```shell script
$ python 3_nested_commands.py list
container (<class 'list'>): []
log (<class 'bool'>): False
log_file (<class 'NoneType'>): None
verbose (<class 'bool'>): False
```

1. ran combined
```shell script
$ python 3_nested_commands.py create directory list
usage: pytest [-h] [-v] [-l] [-o LOG_FILE] {create,remove,list} ...
pytest: error: unrecognized arguments: list
```
