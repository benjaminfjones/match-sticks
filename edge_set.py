"""
API for `Edge`s and `EdgeSet`s.

See README.md for a description of the problem that this code solves.
"""
from __future__ import annotations
from enum import Enum
from typing import Set
import copy
import my_memo


class Orientation(Enum):
    """
    Edge orientation.
    """
    VERTICAL = "Vertical"
    HORIZONTAL = "Horizontal"


class Edge:
    """
    An edge between integer points on the standard unit lattice in R^2.

    - For a Vertical edge, (col, row) is the XY-coordinate of its lower-most point.
    - For a Horizontal edge, (col, row) is the XY-coordinate of its left-most point.
    """
    col: int  # col >= 0, cols vary in width/x dim
    row: int  # row >= 0, rows vary in height/y dim
    orientation: Orientation

    def __init__(self, c: int, r: int, o: Orientation) -> None:
        self.col = c
        self.row = r
        self.orientation = o

    def __copy__(self):
        """
        Copy constructor.
        """
        return EdgeSet(self.height, self.width, set(self.edges))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Edge):
            raise NotImplementedError
        return (
            self.row == other.row and
            self.col == other.col and
            self.orientation == other.orientation
        )

    def __str__(self) -> str:
        return f"Edge({self.col}, {self.row}, {self.orientation})"

    def __hash__(self) -> int:
        return hash((self.col, self.row, self.orientation))

    @staticmethod
    @my_memo.memoize
    def vert_edge(c: int, r: int) -> Edge:
        """
        Static factory method that produces (unique) vertical edges.

        This method is memoized as an optimization. The number of Edges
        constructed while enumerating EdgeSets is very large if done naively.
        Memoization ensures that every `Edge.vert_edge(c, r)` constructed at
        runtime shares memory with every other one at the same position.  """
        return Edge(c, r, Orientation.VERTICAL)

    @staticmethod
    @my_memo.memoize
    def horiz_edge(c: int, r: int) -> Edge:
        """
        Static factory method that produces (unique) horizontal edges.

        This method is memoized as an optimization. The number of Edges
        constructed while enumerating EdgeSets is very large if done naively.
        Memoization ensures that every `Edge.horiz_edge(c, r)` constructed at
        runtime shares memory with every other one at the same position.  """
        return Edge(c, r, Orientation.HORIZONTAL)


# The number of boundary edges that is inadmissible for each unit square on the grid
INADMISSIBLE_BOUNDARY = 3


class EdgeSet:
    """
    A set of horizontal and vertical unit length edges, spanning points on the
    std integer lattice in R^2.

    Horizontal edges are represented by their left-most XY-coordinate and
    vertical edges by their bottom-most coordinate.

    See the README.md for a description of what a "valid" edge set is.

    Invariants:
        - forall e : edges. e.orientation == HORIZONTAL => 0 <= e.row <= height
        - forall e : edges. e.orientation == HORIZONTAL => 0 <= e.col <  width
        - forall e : edges. e.orientation == VERTICAL => 0 <= e.row <  height
        - forall e : edges. e.orientation == VERTICAL => 0 <= e.col <= width
    """
    height: int
    width: int
    edges: Set[Edge]

    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.edges = set()

    def __str__(self):
        return f"EdgeSet(height={self.height}, width={self.width}, {self.edges})"

    def place_horiz_edge(self, col: int, row: int) -> None:
        """
        Update `edge_set` by adding the horizontal edge at (col, row).
        """
        assert 0 <= row and row <= self.height
        assert 0 <= col and col < self.width
        self.edges.add(Edge.horiz_edge(col, row))

    def place_vert_edge(self, col: int, row: int) -> None:
        """
        Update `edge_set` by adding the vertical edges at (col, row).
        """
        assert 0 <= row and row < self.height
        assert 0 <= col and col <= self.width
        self.edges.add(Edge.vert_edge(col, row))

    def place_horiz_stack(self, col: int, row: int) -> None:
        """
        Update `edge_set` by adding all horizontal edges in a stack starting with
        the one at (col, row) and including all edges below it.
        """
        assert 0 <= row and row <= self.height
        assert 0 <= col and col < self.width
        for r in range(row+1):
            self.edges.add(Edge.horiz_edge(col, r))

    def place_vert_stack(self, col: int, row: int) -> None:
        """
        Update `edge_set` by adding all vertical edges in a left-facing stack starting with
        the one at (col, row) and including all edges to the left of it.
        """
        assert 0 <= row and row < self.height
        assert 0 <= col and col <= self.width
        for c in range(col+1):
            self.edges.add(Edge.vert_edge(c, row))

    def is_left_ok(self, col: int, row: int) -> bool:
        """
        Determine if all vertical edges are in the edge set that are to the left
        of the given vertical edge (including itself)
        """
        return all([Edge.vert_edge(c, row) in self.edges for c in range(col)])

    def is_down_ok(self, col: int, row: int) -> bool:
        """
        Determine if all horizontal edges are in the edge set that are below
        the given horizontal edge (not including itself)
        """
        return all([Edge.horiz_edge(col, r) in self.edges for r in range(row)])

    def check_vert_edge_constraint(self, col: int, row: int) -> bool:
        return Edge.vert_edge(col, row) not in self.edges or self.is_left_ok(col, row)

    def check_horiz_edge_constraint(self, col: int, row: int) -> bool:
        return Edge.horiz_edge(col, row) not in self.edges or self.is_down_ok(col, row)

    def check_boundary_constraint(self, col: int, row: int) -> bool:
        boundary = filter(lambda e: e in self.edges, [
            Edge.horiz_edge(col, row),
            Edge.horiz_edge(col, row+1),
            Edge.vert_edge(col, row),
            Edge.vert_edge(col+1, row),
        ])
        return len(tuple(boundary)) != INADMISSIBLE_BOUNDARY

    def check_constraints(self) -> bool:
        """
        For each row, call `is_left_ok` at the right-most present vertical edge.
        Similarly for the columns and horizontal edges.
        """
        # check vert edges
        for row in range(self.height):
            # check columns starting at far right. Note: we don't need to check the 0-th
            # column because there is nothing to the left of it.
            for col in range(self.width, 0, -1):
                if self.check_vert_edge_constraint(col, row):
                    break  # goto next row
                else:
                    return False

        # check horiz edges
        for col in range(self.width):
            for row in range(self.height, 0, -1):
                if self.check_horiz_edge_constraint(col, row):
                    break  # goto next column
                else:
                    return False

        # check unit square constraints
        for row in range(self.height):
            for col in range(self.width):
                if not self.check_boundary_constraint(col, row):
                    return False

        return True

    def embed(self):
        """
        Return a new edge set that is a copy of self, but on a grid one row
        taller.
        """
        larger_set = copy.copy(self)
        larger_set.height += 1
        return larger_set

    def pretty_print(self) -> str:
        """
        Return a pretty printed string representation of the edge set.

        Example:

        ```
        *--*  *
        |
        *  *--*

        *  *--*
        ```
        """
        # Start with a character array that we update in place. The array has
        # 3 characters for each horizontal edge: "*--" and two rows for each
        # logical row (see example above).
        #
        # The first row of the array corresponds to the lowest row in the grid
        # and the first character in each row corresponds to the left-most
        # integer point on that row.
        grid = [[" " for _ in range(3*self.width+1)] for _ in range(2*self.height+1)]
        # draw integer points
        for r in range(self.height+1):
            for c in range(self.width+1):
                x = 3*c
                y = 2*r
                grid[y][x] = "*"
        # fill in edges
        for e in self.edges:
            x = 3*e.col
            y = 2*e.row
            if e.orientation == Orientation.HORIZONTAL:
                grid[y][x+1] = "-"
                grid[y][x+2] = "-"
            else:
                grid[y+1][x] = "|"
        # join the character array, reversing the rows
        row_strings = ["".join(array_row) for array_row in grid]
        return "\n".join(reversed(row_strings))
