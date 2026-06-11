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
--8<-- "examples/comprehensive.py"
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
