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
