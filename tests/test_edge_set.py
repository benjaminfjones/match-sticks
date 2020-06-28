from edge_set import Edge, EdgeSet
import copy
import my_memo


def test_copy():
    e1 = EdgeSet(2, 2)
    e1.place_horiz_edge(0, 1)
    e1.place_horiz_edge(0, 2)
    num_edges = len(my_memo._memoized)
    e2 = copy.copy(e1)
    e2.place_horiz_edge(0, 0)
    assert e1 != e2
    assert len(my_memo._memoized) == num_edges + 1


def test_embed():
    e = EdgeSet(0, 3)
    e.place_horiz_stack(0, 0)
    e.place_horiz_stack(2, 0)
    f = e.embed()
    assert f.height == e.height + 1
    assert f.width == e.width
    assert f.edges == e.edges


def test_memoizer():
    my_memo._memoized = type(my_memo._memoized)()
    e1 = Edge.vert_edge(0, 0)
    e2 = Edge.vert_edge(0, 0)
    assert e1 == e2
    assert id(e1) == id(e2)

    e3 = Edge.horiz_edge(0, 0)
    assert e1 != e3
    e4 = Edge.vert_edge(1, 0)
    assert e1 != e4

    assert len(my_memo._memoized) == 3

    Edge.vert_edge(1, 0)
    Edge.horiz_edge(0, 0)
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


def test_validate_stack():
    """
    Validate (or not) the four 2x2 examples in the README.
    """
    # empty grid
    e = EdgeSet(2, 2)
    assert e.check_constraints()  # empty grids are always valid

    # invalid grid
    e = EdgeSet(2, 2)
    e.place_horiz_stack(1, 1)
    e.place_vert_stack(0, 1)
    e.place_horiz_edge(0, 2)
    assert not e.is_down_ok(0, 2)
    assert e.is_down_ok(1, 1)
    assert not e.check_constraints()  # missing horizontal edges below (0, 2)

    # invalid attempted fix
    e = EdgeSet(2, 2)
    e.place_horiz_stack(1, 1)
    e.place_vert_stack(0, 1)
    e.place_horiz_stack(0, 2)  # "fix" by adding an edge
    assert e.is_down_ok(0, 2)
    assert e.is_down_ok(1, 1)
    # stacks are ok, but square constraint is not for upper-left square
    assert not e.check_constraints()

    # valid attempted fix!
    e = EdgeSet(2, 2)
    e.place_horiz_stack(1, 1)
    e.place_vert_stack(1, 1)  # fix by switching vert stack from (0, 1) to (1, 1)
    e.place_horiz_stack(0, 2)
    assert e.check_constraints()  # fixed!


def test_pretty_print():
    """
    Recreate one of the valid 2x2 edge sets from the README.
    """
    e = EdgeSet(2, 2)
    e.place_horiz_stack(0, 2)
    e.place_horiz_stack(1, 1)
    e.place_vert_stack(1, 1)
    print(e.pretty_print())
    expected = """*--*  *
|  |   
*--*--*
       
*--*--*"""  # noqa: W291,W293
    assert e.pretty_print() == expected
