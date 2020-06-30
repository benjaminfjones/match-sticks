from itertools import combinations
import util


def test_subsets():
    alist = [1, 2, 3]
    subs = util.subsets(alist)
    assert () in subs
    assert (1,) in subs
    assert (2,) in subs
    assert (3,) in subs
    assert (1, 2) in subs
    assert (1, 3) in subs
    assert (2, 3) in subs
    assert (1, 2, 3) in subs

    for i in range(5):
        alist = list(range(i))
        assert len(list(util.subsets(alist))) == 2**i


def test_binomial():
    N = 5  # test subsets of size 0..4
    for size in range(N):
        for subsize in range(N):
            myset = list(range(size))
            num_subsets = sum(1 for _ in combinations(myset, subsize))
            assert util.binomial(size, subsize) == num_subsets
