
# coding: utf-8
from jsonpickle import encode, decode
from typing import Any

def dump(obj : Any, filename : str, *args, **kwargs) -> None:
    with open(filename, 'w') as file:
        file.write(encode(obj, *args, **kwargs))

def load(filename: str, *args, **kwargs) -> Any:
    with open(filename, 'r') as file:
        return decode(file.read(), *args, **kwargs)
