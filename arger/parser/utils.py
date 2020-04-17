from typing import List, Set


def _generate_options():
    """Coroutine to identify short options that haven't been used yet.

    Yields lists of short option (if available) and long option for
    the given name, keeping track of which short options have been previously
    used.
    If you aren't familiar with coroutines, use similar to a generator:
    x = _generate_options()
    next(x)  # advance coroutine past its initialization code
    params = x.send(param_name)
    """
    used_short_options: Set[str] = set()
    param_name = yield
    while True:
        names = ["--" + param_name]
        for letter in param_name:
            if letter not in used_short_options:
                used_short_options.add(letter)
                names.insert(0, "-" + letter)
                break
        param_name = yield names


def generate_flags(
    param: str, param_doc: List[str], option_generator,
):
    names = []

    while param_doc and param_doc[0].startswith("-"):
        names.append(param_doc.pop(0))

    return names if names else option_generator.send(param)


def get_option_generator():
    option_generator = _generate_options()
    next(option_generator)
    return option_generator
