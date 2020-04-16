# Multiple Commands

in a file named `main.py`

```python
--8<-- "multi_functions.py"
```

## Run help
```sh
$ python main.py -h
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

## Run `create` help
```sh
$ python main.py create -h
usage: pytest create [-h] name

positional arguments:
  name        Name of the test

optional arguments:
  -h, --help  show this help message and exit
```

## Run `remove` help
```sh
$ python main.py remove -h
usage: pytest remove [-h] [name [name ...]]

positional arguments:
  name        tests to remove

optional arguments:
  -h, --help  show this help message and exit
```

## Run `list` help
```sh
$ python main.py list -h
usage: pytest list [-h]

optional arguments:
  -h, --help  show this help message and exit
```


## Run `create`
```sh
$ python main.py create direcory
name (<class 'str'>): direcory
```


## Run `remove`
```sh
$ python main.py remove direcory
name (<class 'tuple'>): ('direcory',)
```


## Run `list`
```sh
$ python main.py list
container (<class 'list'>): []
```

## Run combined
```sh
$ python main.py create directory list
usage: pytest [-h] {create,remove,list} ...
pytest: error: unrecognized arguments: list
```
