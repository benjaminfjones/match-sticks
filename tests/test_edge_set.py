from edge_set import Edge, EdgeSet
import my_memo


def test_memoizer():
    e1 = Edge.vert_edge(0, 0)
    e2 = Edge.vert_edge(0, 0)
    assert e1 == e2
    assert id(e1) == id(e2)

    e3 = Edge.horiz_edge(0, 0)
    assert e1 != e3
    e4 = Edge.vert_edge(1, 0)
    assert e1 != e4

    assert len(my_memo._memoized) == 3

    e5 = Edge.vert_edge(1, 0)
    e6 = Edge.horiz_edge(0, 0)
    assert len(my_memo._memoized) == 3

    
def test_place_horiz():
    e = EdgeSet(2, 2)
    e.place_horiz_stack(0, 1)
    assert Edge.horiz_edge(0, 0) in e.edges
    assert Edge.horiz_edge(0, 1) in e.edges
    assert Edge.horiz_edge(0, 2) not in e.edges
    assert Edge.horiz_edge(1, 0) not in e.edges
    assert Edge.horiz_edge(1, 1) not in e.edges
    assert Edge.horiz_edge(1, 2) not in e.edges

    assert e.is_down_ok(0, 0)
    assert e.is_down_ok(0, 1)
    assert e.is_down_ok(0, 2)
    assert e.is_down_ok(1, 0)
    assert not e.is_down_ok(1, 1)
    assert not e.is_down_ok(1, 2)


def test_place_vert():
    e = EdgeSet(2, 2)
    e.place_vert_stack(0, 1)
    assert e.edges == {Edge.vert_edge(0, 1)}

    assert e.is_left_ok(0, 1)
    assert e.is_left_ok(1, 1)
    assert not e.is_left_ok(2, 1)

    e = EdgeSet(2, 2)
    e.place_vert_stack(1, 0)
    assert e.edges == {Edge.vert_edge(0, 0), Edge.vert_edge(1, 0)}

    assert e.is_left_ok(0, 0)
    assert e.is_left_ok(1, 0)
    assert e.is_left_ok(2, 0)
    assert e.is_left_ok(0, 1)
    assert not e.is_left_ok(1, 1)
    assert not e.is_left_ok(2, 1)
    assert e.is_left_ok(0, 2)
    assert not e.is_left_ok(1, 2)
    assert not e.is_left_ok(2, 2)