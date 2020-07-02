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

    Time complexity is O(log_b(z)).

    TODO:
        - document parameters, all non-negative ints
        - describe what this counts
    """
    ds = digits(z, base=b)
    n_zeros = 0
    if j in ds:
        ds = ds[:ds.index(j)]
    else:
        if m <= len(ds):
            ds = ds[:m]
        else:
            n_zeros = m - len(ds)
    return sum(1 for d in ds if d <= j) + n_zeros + 2


def count_valid_edge_sets(m: int, n: int) -> int:
    """
    Return the number of valid edge sets in the `m` x `n` rectangular grid.

    Example:

    >>> [count_valid_edge_sets(i, i) for i in range(7)]
    [1, 7, 115, 3451, 164731, 11467387, 1096832395]

    Try this and go get a cup of coffee:

    >>> count_valid_edge_sets(8, 8)
    22111390122811
    """
    if n == 0:
        return 2**m
    return sum(
        (
            reduce(lambda x, y: x*y, (count(i, j, n+2, m) for j in range(1, n+1)))
            for i in range((n+2)**m)
        )
    )
