# Setup

## Requirements

* Make:
    * macOS: `$ xcode-select --install`
    * Linux: [https://www.gnu.org/software/make](https://www.gnu.org/software/make)
    * Windows: [https://mingw.org/download/installer](https://mingw.org/download/installer)
* Python: `$ pyenv install`
* PDM: [https://pdm.fming.dev/latest/](https://pdm.fming.dev/latest/)


## Installation

Install project dependencies into a virtual environment:

```text
$ pdm install
```

# Development Tasks

## Manual

Run the tests:

```text
$ pytest
```

Run static analysis:

```text
$ pre-commit run -a
```

Build the documentation:

```text
$ pdm run serve-docs
```

# Release

To create a new release

```text
$ python tasks.py release
```
