from collections import OrderedDict
from typing import Dict, Optional

from .parser import opterate
from .types import F, VarArg


class Command:
    def __init__(self, fn: Optional[F] = None):
        self._fn = fn  # only the root element may not have a function associated.
        self.name: Optional[str] = fn.__name__ if fn else None
        self.desc, self.args = opterate(self._fn) if fn else ("", dict())
        self._sub: Dict[str, "Command"] = OrderedDict()

    def is_valid(self) -> bool:
        return bool(self._fn or len(self._sub))

    # def callback(self, ns):
    #     self.namespace = ns

    def run(self, command: Optional[str] = None, **kwargs):
        root_kwargs = {k: v for k, v in kwargs.items() if k in set(self.args)}
        cmd_kwargs = {k: v for k, v in kwargs.items() if k not in set(self.args)}

        results = OrderedDict()
        if root_kwargs and self.name:
            results[self.name] = self(**root_kwargs)
        if command:
            results[command] = self._sub[command](**cmd_kwargs)
        return results

    def __call__(self, *args, **kwargs):
        if self._fn:
            if not args:
                for k in list(kwargs):
                    if k in self.args and isinstance(
                        self.args[k].kwargs.get("type"), VarArg
                    ):
                        args = kwargs.pop(k)
            return self._fn(*args, **kwargs)
        raise NotImplementedError("No function to dispatch")

    def add(self, func: F) -> "Command":
        cmd = Command(func)
        if cmd.name in self._sub:
            raise KeyError(f"Already defined a command named {cmd.name}")
        self._sub[func.__name__] = cmd
        return cmd

    def __iter__(self):
        yield from self._sub.items()
