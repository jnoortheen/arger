from typing import Any, Callable, TypeVar


F = TypeVar('F', bound=Callable[..., Any])

UNDEFINED = object()
"""sometimes the value could be None. we need this to distinguish such values."""
