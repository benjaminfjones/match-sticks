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
