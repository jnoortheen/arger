# Concepts
A command/sub-command is parsed from function.
    
## Function
Function's signature is used to create parser

### 1. Positional Arguments:
Positional arguments become mandatory.

### 2. Keyword Arguments:
All keyword arguments in the function definition are options.
Arbitrary args and values can be captured with **kwargs

### 3. type annotations:
used to determine the type and action of the arguments.

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

## Arger

::: arger.Arger
    
## Argument

::: arger.Argument

## Option

::: arger.Option

