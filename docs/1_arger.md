# Arger
    
## Function
Function's signature is used to create generate parser arguments.

### 1. Positional Arguments:
Positional parameters become mandatory and reperesented by `arger.Argument`.

### 2. Keyword Arguments:
All keyword arguments in the function definition are `arger.Option` 
and they are optional by default.

### 3. type annotations:
used to determine the type and action of the arguments. 
The function will be dispatched with values converted to the respective types.

For example:

| Parameter Annotation      |      parser.add_argument   | note |
|---------------------------|:--------------------------:|------|
| def fn(a:str):...             |  dest='a', type=str | |
| def fn(a:int):...             |  dest='a', type=int | |
| def fn(a:Tuple[str, ...]):... |  dest='a', nargs='+' | one or more|
| def fn(a:Tuple[str, str]):... |    dest='a', nargs=2   | consumes 2 positional arguments |
| def fn(a:tuple=())           |    dest='a', nargs='*', default=()   | 0 or more args consumes |
| def fn(a:List[str])           |    dest='a', nargs='*'   | same as tuple |

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
