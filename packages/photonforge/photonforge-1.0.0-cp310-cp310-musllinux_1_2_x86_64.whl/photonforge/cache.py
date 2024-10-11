import collections as _col
import pathlib as _pth
import typing as _typ


path: str = "~/.tidy3d/pf_cache"


def _cache_path(name: str) -> _pth.Path:
    return _pth.Path(path).expanduser() / name[:3]


class _Cache:
    def __init__(self, size: int) -> None:
        self.size = size
        self.data = _col.OrderedDict()

    def __getitem__(self, key: _typ.Any) -> _typ.Any:
        value = self.data.get(key, None)
        if value is not None:
            self.data.move_to_end(key)
        return value

    def __setitem__(self, key: _typ.Any, value: _typ.Any) -> None:
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if self.size > 0:
            while len(self.data) >= self.size:
                self.data.popitem(False)

    def clear(self) -> None:
        self.data = _col.OrderedDict()
