from edge_set import Edge, EdgeSet
from typing import Generator
from itertools import combinations


def enumerate_edge_sets(height: int, width: int) -> Generator[EdgeSet, None, None]:
    """
    Recursively enumerate valid edge sets.

    This function recurses on the number of rows in the parent grid. The base
    case of a single row is handled by a helper function.

    The reason recursive enumeration works is that given a grid of positive
    height, all valid edge sets of any sub-grid of strictly smaller height,
    and sharing the lower-left corner, are also valid on the full grid.
    Conversely, every valid edge set on the full grid can be intersected with
    a grid of smaller height (sharing the lower-left corner) to produce a
    valid edge set on the small grid.

    For example, consider the following valid edge set of height 0:

    *--*  *

    In the 1x2 grid, it is also valid:

    *  *  *

    *--*  *

    Indeed, the downward stack condition is met because we haven't added any
    edges and it was already satisfied in the 0x2 grid. Same with the
    horizontal stack condition (vacuously). Finally, the unit square boundary
    condition is satisfied for both squares, because they can have at most 1
    edge.

    The larger valid edge set can then be extended to all possible edge sets
    containing the original by adding edges and checking the constraints.

    Similarly, given a valid edge set of a 1x2 grid:

    *  *--*
    |
    *--*--*

    The intersection with the lower-left 0x2 grid is also valid:

    *--*--*

    because the stack conditions are preserved by remove all squares above a
    row or to the right of any column. Also, the square boundary condition is
    preserved because the boundary edges of squares in the small grid are
    exactly the same as in the full grid.
    """
    if height == 0:
        yield from enumerate_height_zero(width)
    else:
        raise NotImplementedError


def enumerate_height_zero(width: int) -> Generator[EdgeSet, None, None]:
    """
    Directly enumerate valid edge sets of height zero (the grid is the integer
    points on a horizontal line segment).

    In this case, there are only horizontal edges, and all combinations are valid.
    """
    columns = list(range(width))
    for num_edges in range(width+1):
        for combo in combinations(columns, num_edges):
            es = EdgeSet(0, width)
            for col in combo:
                es.edges.add(Edge.horiz_edge(col, 0))
            yield es
