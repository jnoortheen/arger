## v1.0.7 (2020-11-09)

### Refactor

- merge funcs and maian modules
- remove ParsedFunc type
- merge classes that handle Argument and Option creation
- update TypeAction handling VarArg
- replace namedtuple Param with inspect.Parameter
- merge into single module parsers
- update Argument update funcs
- reduce number of modules
- update usage of types inside docstrings
- move code from types to typing_utils

### Feat

- add version flag/action by passing version string to Arger
- create subcommands as soon as Arger initiated
- publish docs to github-pages

## v1.0.6 (2020-11-02)

### Feat

- add python 3.9 support

## v1.0.5 (2020-11-02)

## v1.0.3 (2020-11-02)

### Feat

- implement skipping private arguments

## v1.0.2 (2020-11-01)

### Feat

- add py39 to ci tests

## v1.0.1 (2020-11-01)

### Feat

- first stable release
- any level of nested commands will get dispatched
- use notebook for testing examples

### Fix

- py36 compat with re.Pattern

### Refactor

- rewrite arger using new docstring parser
- update docstring parser and add tests
- remove external dependency to parse docstring

## v0.4.1 (2020-04-18)

### Fix

- mypy errors

## v0.4.0 (2020-04-18)

### Fix

- py36 compatibility
- variable arg handling

### Refactor

- inherit Option from Argument
- update typing-utils to work on py36
- update parser functions

### Feat

- add support for more complex types
- add for tuple/list support

## v0.3.0 (2020-04-16)

### Feat

- implement mkdocs
- add support for variadict arguments

### Refactor

- reduce complexity in parser function

## v0.2.4 (2020-04-15)

### Fix

- setting flags only when not defined

## v0.2.3 (2020-04-15)

### Fix

- using option to define arguments

### Feat

- use Option for populating arguments

### Refactor

- rename arger class module

## v0.2.2 (2020-04-13)

## v0.2.1 (2020-04-13)

### Fix

- handle tests passing sys.argv

## v0.2.0 (2020-04-13)

### Feat

- sub-command with a root context function
- add python < 37 compatible type checks
- call nested commands
- add ability to add nested commands

## v0.1.3 (2020-04-11)

## v0.1.2 (2020-04-11)

## v0.1.1 (2020-04-11)

## 0.1 (2020-04-11)

### Fix

- recognise type from typehint and default value
- mypy type errors
- test workflow

### Feat

- implement single function dispatch
- make arger work with single or multi functions
- implement parser
- add action to publish package
- add github actions for testing and linting
- add boilerplate from

### Refactor

- add arger structs
- remove notebooks folder
- move out docstring to sub functions
