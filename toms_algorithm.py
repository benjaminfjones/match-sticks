"""
Evaluate Tom's Algorithm for counting valid edge sets.

`count` and `count_valid_edge_sets` are due to Tom Edgar (edgartj@plu.edu).
"""
from functools import reduce
from typing import List


def digits(z: int, base=10) -> List[int]:
    """
    Return the list of digits of `z` in base `base`, least significant digits first.

    Base `base` digits are represented as integers.

    Examples:

    >>> digits(10, base=2)
    [0, 1, 0, 1]
    >>> digits(10)
    [0, 1]
    >>> digits(116, base=31)
    [23, 3]
    """
    res = []
    while True:
        q, r = divmod(z, base)
        res.append(r)
        if q == 0:
            return res
        z = z // base


def count(z: int, j: int, b: int, m: int) -> int:
    """
    Count something mysterious.

    TODO:
        - document parameters
        - describe what this counts
    """
    ds = digits(z, base=b)
    if j in ds:
        b_len = ds.index(j)
    else:
        b_len = m
    ds.extend((m-len(ds))*[0])
    ds_lt_j = [i for i in range(b_len) if ds[i] <= j]
    return len(ds_lt_j) + 2


def count_valid_edge_sets(m: int, n: int) -> int:
    """
    Return the number of valid edge sets in the `m` x `n` rectangular grid.

    Example:

    >>> [ValidMatchsticks(i,i) for i in [0..6]]
    [1, 7, 115, 3451, 164731, 11467387, 1096832395]
    """
    if n == 0:
        return 2**m
    return sum(
        (
            reduce(lambda x, y: x*y, (count(i, j, n+2, m) for j in range(1, n+1)))
            for i in range((n+2)**m)
        )
    )
