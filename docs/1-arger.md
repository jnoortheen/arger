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
import arger
from typing import *
from enum import Enum

# Type -> resulting `arger.add_argument` method call

def _(
a_st:str,              # -> add_argument(dest='a', type=str)
a_in:int,              # -> add_argument(dest='a', type=int)
a_tp:Tuple[int, ...],  # -> add_argument(dest='a', type=int, nargs='+') : one or more
a_tp_int:Tuple[int, int],  # -> add_argument(dest='a', type=int, nargs='2') : consumes 2 positional
a_ls:List[int],        # -> add_argument(dest="a", type=int, nargs="*") : zero or more
a_opt:Optional[int],    # -> add_argument(dest="a", type=int, nargs="?") : zero or one positional
a_en:Enum(
    'AnySubClsOfEnum',
    'ONE TWO'
    ),               # -> add_argument(dest="a", choices=list(cls), type=lambda x: cls[x]) : accepts str from cli and returns as an Enum.
a_lt: Literal[
    'one', 'two'
],                  # -> add_argment(dest="a_lt", choices=["one", "two"], type=str) : accepts str from cli and returns the same
a_lt_in: Literal[
    1, 2
],                  # -> add_argment(dest="a_lt", choices=[1, 2], type=int) : accepts str from cli and returns int
a_cs2:Annotated[
    int, # -> Argument's type argument. also satisfies type checkers
    arger.Argument(
        metavar="INT",
        action=ActionSubCls
)],                 # -> add_argument(dest="a", metavar="INT", type=int, action=ActionSubCls) : all the arguments to the `Argument` will get delegated to add_argument
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
