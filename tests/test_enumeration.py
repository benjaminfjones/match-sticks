from enumerate_edge_sets import naively_enumerate_edge_sets, enumerate_edge_sets
from util import binomial


def test_Nx0_naive():
    """
    The Nx0 (N >= 0) grid has 2^N valid edge sets (all sets are valid).
    """
    for n in range(6):
        expected = 2**n
        actual = sum(1 for _ in naively_enumerate_edge_sets(n, 0))
        assert actual == expected


def test_Nx0_recursive():
    """
    The Nx0 (N >= 0) grid has 2^N valid edge sets (all sets are valid).
    """
    for n in range(6):
        expected = 2**n
        actual = sum(1 for _ in enumerate_edge_sets(n, 0))
        assert actual == expected


def test_Nx1_naive():
    """
    The Nx1 (N >= 0) grid has 3^(N+1) - 2^N valid edge sets. See,

    Donald E. Knuth, The Art of Computer Programming, Vol. 4, fascicle 1,
    section 7.1.4, pp. 134, 138, 139, 219, answer to exercise 172,
    Addison-Wesley, 2009.

    and

    https://oeis.org/A083313
    """
    for n in range(6):
        expected = 3**(n+1) - 2**n
        actual = sum(1 for _ in naively_enumerate_edge_sets(n, 1))
        assert actual == expected


def test_NxN_naive():
    """
    If a(N) = the number of valid edge sets on the NxN grid for N >= 0, then a(N) is the sequence:

    a(N) = Sum_{k=0..n+1} k^(n+1) * Sum_{j=0..k} (-1)^(n+1+k-j) * binomial(k, j) * (k-j)^(n+1).

    See: https://oeis.org/A220181
    """
    # Note: for n == 3, this takes ~4 mins to run
    for n in range(3):
        expected = sum(k**(n+1) * sum((-1)**(n+1+k-j) * binomial(k, j) * (k-j)**(n+1)
                                      for j in range(k+1))
                       for k in range(n+2))
        actual = sum(1 for _ in naively_enumerate_edge_sets(n, n))
        assert actual == expected
