from itertools import chain, combinations
from typing import Generator, Iterable, Tuple, TypeVar


T = TypeVar('T')


def subsets(iterable: Iterable[T]) -> Generator[Tuple[T, ...], None, None]:
    """
    Consume the given iterator and return all possible subsets of it as tuples.
    """
    things = list(iterable)
    n = len(things)
    yield from chain(*[combinations(things, i) for i in range(n+1)])


def binomial(n: int, k: int) -> int:
    """
    Return the binomial coefficient `n choose k`.
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        nprime = n
        for t in range(1, min(k, n - k) + 1):
            ntok *= nprime
            ktok *= t
            nprime -= 1
        return ntok // ktok
    else:
        return 0
