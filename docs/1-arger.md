# Arger

## Function
Function's signature is used to create generate parser arguments.

### 1. Positional Arguments:
Positional parameters become mandatory.

### 2. Optional Arguments:
All keyword arguments (ones with default value) in the function become flags/optionals.

### 3. type annotations:
used to determine the type and action of the arguments.
The function will be dispatched with values converted to the respective types.  
**Note**: Use `arger.Argument` class as annotation in case you want to pass values to `parser.add_argument`.

For example:

```py
# Type -> resulting `arger.add_argument` method call

def _(
a:str,              # -> add_argument(dest='a', type=str)
a:int,              # -> add_argument(dest='a', type=int)
a:Tuple[int, ...],  # -> add_argument(dest='a', type=int, nargs='+') : one or more
a:Tuple[int, int],  # -> add_argument(dest='a', type=int, nargs='2') : consumes 2 positional
a:List[int],        # -> add_argument(dest="a", type=int, nargs="*") : zero or more
a:Optional[int],    # -> add_argument(dest="a", type=int, nargs="?") : zero or one positional
a:Enum(
    'AnySubClsOfEnum',
    'ONE TWO'
    ),               # -> add_argument(dest="a", choices=["ONE", "TWO"]) : accepts str from cli and returns as an Enum.
a:cast(
    int,
    ActionSubCls
),                  # -> add_argument(dest="a", action=ActionSubCls)
a:cast(
    int,
    arger.Argument(
        metavar="INT",
        type=int,
        action=ActionSubCls
)),                 # -> add_argument(dest="a", metavar="INT", type=int, action=ActionSubCls) : all the arguments to the `Argument` will get delegated to add_argument
kwarg:int = 0,      # -> add_argument("--kwarg", "-k", dest="kwarg", type=int, default=0)
):...
```

### 4. Docstring (ReST or GoogleDoc)
- The top part of the docstring becomes the usage message for the command.
- Parameter docstrings become help message for the arguments/options of the command.
- Rest of the docstrings passed as `epilog` to the parser.
- ReST/GoogleDoc-style/NumpyDoc-style are supported
- Options-strings can further be defined in the docstring.

```pydocstring
Args:
    name: [short option and/or long option] help text
    variable_name: -v --verbose the help_text for the variable
    variable_name: -v the help_text no long option
    variable_name: --verbose the help_text no short option
```
