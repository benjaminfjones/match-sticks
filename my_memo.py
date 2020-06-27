"""
A very simple memoizer.

I should probably just use the `lru_cache` builtin one, but <shrug/>
"""
from typing import Any, Dict, Tuple

# global memoization table
_memoized: Dict[Tuple[Any, Any, Any, Any], Any] = {}


def get_id_tuple(f, args, kwargs, mark=object()):
    """
    Generate a unique key for a specific call.
    """
    id_list = [id(f)]
    for arg in args:
        id_list.append(id(arg))
    id_list.append(id(mark))
    for k, v in kwargs:
        id_list.append(k)
        id_list.append(id(v))
    return tuple(id_list)


def memoize(f):
    """
    A basic class memoizer.

    This can be used to decorate a class (meaning every method), or single
    methods/functions.
    """
    def memoized(*args, **kwargs):
        key = get_id_tuple(f, args, kwargs)
        if key not in _memoized:
            _memoized[key] = f(*args, **kwargs)
        return _memoized[key]
    return memoized
