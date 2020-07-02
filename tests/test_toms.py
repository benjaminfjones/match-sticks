from toms_algorithm import digits, count_valid_edge_sets
import random


def test_digits():
    """
    Test some simple digits calls.
    """
    assert digits(10, base=2) == [0, 1, 0, 1]
    assert digits(10) == [0, 1]
    assert digits(116, base=31) == [23, 3]


def test_random_digits():
    """
    Compute digits of random ints for random bases and compare the resulting power sum
    to the original random int.
    """
    n_tests = 20
    for _ in range(n_tests):
        z = random.randint(1, 10000)
        base = random.randint(2, 100)
        ds = digits(z, base=base)
        assert z == sum(d*base**n for n, d in enumerate(ds))


def test_toms_Nx1():
    max_N = 5
    assert [count_valid_edge_sets(n, 1) for n in range(max_N+1)] == [2, 7, 23, 73, 227, 697]


def test_toms_NxN():
    max_N = 5
    assert (
        [count_valid_edge_sets(n, n) for n in range(max_N+1)] == [1, 7, 115, 3451, 164731, 11467387]
    )


def test_symmetry():
    """
    Assert that count_valid_edge_sets(m, n) == count_valid_edge_sets(n, m) for
    a range of small m, n.
    """
    max_N = 6
    for m in range(max_N):
        for n in range(m):
            assert count_valid_edge_sets(m, n) == count_valid_edge_sets(n, m)
