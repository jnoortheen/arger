# Supported function argument type annotations
in a file named `main.py`

```python
--8<-- "supported_options.py"
```

##  ran empty
```sh
$ python main.py
```

## ran `help`
```sh
$ python main.py --help
usage: pytest [-h] {cmd1,cmd2} ...

App Description goes here

optional arguments:
  -h, --help   show this help message and exit

commands:
  {cmd1,cmd2}
    cmd1       Example function with types documented in the docstring.
    cmd2       A script with three optional values.
```

## ran `cmd1` help

```sh
$ python main.py cmd1 --help
usage: pytest cmd1 [-h] [-a {one,two}] [-o OPTIONAL_STR] [-p OPTIONAL_INT] [-t [OPTIONAL_TPL [OPTIONAL_TPL ...]]]
                   an_int an_str a_tuple a_tuple a_tuple a_var_tuple [a_var_tuple ...]

positional arguments:
  an_int
  an_str
  a_tuple
  a_var_tuple

optional arguments:
  -h, --help            show this help message and exit
  -a {one,two}, --an_enum {one,two}
  -o OPTIONAL_STR, --optional_str OPTIONAL_STR
  -p OPTIONAL_INT, --optional_int OPTIONAL_INT
  -t [OPTIONAL_TPL [OPTIONAL_TPL ...]], --optional_tpl [OPTIONAL_TPL [OPTIONAL_TPL ...]]
```

## ran `cmd1` with only required

```sh
$ python main.py cmd1 10 str1 tp1 tp2 tp3 vtp1
a_tuple (<class 'tuple'>): ('tp1', 'tp2', 'tp3')
a_var_tuple (<class 'tuple'>): ('vtp1',)
an_enum (<enum 'Choice'>): Choice.one
an_int (<class 'int'>): 10
an_str (<class 'str'>): str1
optional_int (<class 'int'>): 0
optional_str (<class 'str'>): 
optional_tpl (<class 'tuple'>): ()
```

## ran `cmd1` with valid arguments

```sh
$ python main.py cmd1 10 str1 tp1 tp2 tp3 vtp1 -t otp1 otp2 -o ostr -p 100 -a two
a_tuple (<class 'tuple'>): ('tp1', 'tp2', 'tp3')
a_var_tuple (<class 'tuple'>): ('vtp1',)
an_enum (<enum 'Choice'>): Choice.two
an_int (<class 'int'>): 10
an_str (<class 'str'>): str1
optional_int (<class 'int'>): 100
optional_str (<class 'str'>): ostr
optional_tpl (<class 'tuple'>): ('otp1', 'otp2')
```

## ran `cmd2` help
```sh
$ python main.py cmd2 --help
usage: pytest cmd2 [-h] [-m] [-y] [--my] [a_list [a_list ...]]

positional arguments:
  a_list       catch all positional arguments

optional arguments:
  -h, --help   show this help message and exit
  -m, --m_opt  the m_opt helptext
  -y, --y_opt  the y_opt helptext
  --my         the my helptext
```

## ran `cmd2` with args
```sh
$ python main.py cmd2 10 100 1000
a_list (<class 'list'>): [10, 100, 1000]
m_opt (<class 'bool'>): False
my (<class 'bool'>): False
y_opt (<class 'bool'>): False
```

