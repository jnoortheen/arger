# Usages

in a file named `main.py`

```python
--8<-- "nested_commands.py"
```

## Run help
```sh
$ python main.py -h
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

## Run create help
```sh
$ python main.py create -h
usage: pytest create [-h] name

positional arguments:
  name        Name of the test

optional arguments:
  -h, --help  show this help message and exit
```

## Run remove help
```sh
$ python main.py remove -h
usage: pytest remove [-h] name

positional arguments:
  name        Name of the test

optional arguments:
  -h, --help  show this help message and exit
```

## Run list help
```sh
$ python main.py list -h
usage: pytest list [-h]

optional arguments:
  -h, --help  show this help message and exit
```


## Run create
```sh
$ python main.py create direcory
log (<class 'bool'>): False
log_file (<class 'NoneType'>): None
name (<class 'str'>): direcory
verbose (<class 'bool'>): False
```


## Run remove
```sh
$ python main.py remove direcory
log (<class 'bool'>): False
log_file (<class 'NoneType'>): None
name (<class 'str'>): direcory
verbose (<class 'bool'>): False
```


## Run list
```sh
$ python main.py list
container (<class 'list'>): []
log (<class 'bool'>): False
log_file (<class 'NoneType'>): None
verbose (<class 'bool'>): False
```

## Run combined
```sh
$ python main.py create directory list
usage: pytest [-h] [-v] [-l] [-o LOG_FILE] {create,remove,list} ...
pytest: error: unrecognized arguments: list
```
