def get_id_tuple(f, args, kwargs, mark=object()):
    """ 
    Generate a unique key for a specific call.
    """
    l = [id(f)]
    for arg in args:
        l.append(id(arg))
    l.append(id(mark))
    for k, v in kwargs:
        l.append(k)
        l.append(id(v))
    return tuple(l)

_memoized = {}
def memoize(f):
    """ 
    A basic class memoizer.
    """
    def memoized(*args, **kwargs):
        key = get_id_tuple(f, args, kwargs)
        if key not in _memoized:
            _memoized[key] = f(*args, **kwargs)
        return _memoized[key]
    return memoized