from __future__ import annotations

import argparse
from enum import Enum
from typing import Generator, Set

import my_memo


class Orientation(Enum):
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
        return Edge(c, r, Orientation.VERTICAL)

    @staticmethod
    @my_memo.memoize
    def horiz_edge(c: int, r: int) -> Edge:
        return Edge(c, r, Orientation.HORIZONTAL)


class EdgeSet:
    """
    A set of horizontal and vertical unit length edges, spanning points on the
    std integer lattice in R^2.

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

    def validate_stacks(self) -> bool:
        """
        For each row, call `is_left_ok` at the right-most vertical edge, and
        similarly for the columns and horizontal edges.
        """
        for row in range(self.height):
            for col in range(self.width+1, -1, -1):
                if Edge.vert_edge(col, row) in self.edges:
                    if not self.is_left_ok(col, row):
                        return False
                    else:
                        break  # goto next row

        for col in range(self.width):
            for row in range(self.height+1, -1, -1):
                if Edge.horiz_edge(col, row) in self.edges:
                    if not self.is_down_ok(col, row):
                        return False
                    else:
                        break  # goto next col
        return True


def enumerate_edge_sets(height: int, width: int) -> Generator[EdgeSet, None, None]:
    # TODO
    yield EdgeSet(0, 0)


# --- Main ---

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "height",
        type=int,
        metavar="HEIGHT",
        help="height of the grid"
    )
    parser.add_argument(
        "width",
        type=int,
        metavar="WIDTH",
        help="width of the grid"
    )

    args = parser.parse_args()

    print(f"Enumerating match sticks on {args.height} x {args.width} grid")
    print(f"Number of valid edge sets: {len(list(enumerate_edge_sets(2, 2)))}")


if __name__ == '__main__':
    main()
