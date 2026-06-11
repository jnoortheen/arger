# Arger

## Function
A function's signature is used to generate parser arguments.

### 1. Positional Arguments:
Positional parameters become mandatory arguments.

### 2. Optional Arguments:
All keyword arguments (those with a default value) in the function become flags/optionals.

### 3. Type Annotations:
They are used to determine the type and action of the arguments.
The function will be dispatched with values converted to their respective types.
**Note**: Use the `arger.Argument` class as an annotation if you want to pass values to `parser.add_argument`.

For example:

```py
--8<-- "examples/comprehensive.py"
```

### 4. Docstring (ReST or GoogleDoc)
- The top part of the docstring becomes the usage message for the command.
- Parameter docstrings become help messages for the arguments/options of the command.
- The rest of the docstring is passed as `epilog` to the parser.
- [ReST](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)/[GoogleDoc](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)/[NumpyDoc](https://www.sphinx-doc.org/en/master/usage/extensions/example_numpy.html) formats are supported.
- Custom flags can be defined in the docstring itself.

```pydocstring
Args:
    name: [short option and/or long option] help text
    variable_name: -v --verbose the help_text for the variable
    variable_name: -v the help_text no long option
    variable_name: --verbose the help_text no short option
```
