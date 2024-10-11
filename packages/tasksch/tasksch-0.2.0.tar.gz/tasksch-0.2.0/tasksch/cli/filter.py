import re
import typing as t


def create_filter(rx: str | None, default: bool = True) -> t.Callable[[str], bool]:
    if not rx:
        return lambda x: default
    _rx = re.compile(rx)

    def _matcher(path: str) -> bool:
        return _rx.match(path) is not None

    return _matcher
