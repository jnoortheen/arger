from typing import Iterator, Set


class FlagsGenerator:
    """To identify short options that haven't been used yet based on the parameter name."""

    def __init__(self):
        self.used_short_options: Set[str] = set()

    def generate(self, param_name: str) -> Iterator[str]:
        long_flag = "--" + param_name.replace('_', '-')
        for letter in param_name:
            if letter not in self.used_short_options:
                self.used_short_options.add(letter)
                yield "-" + letter
                break

        yield long_flag
