# match-sticks

![Python package](https://github.com/benjaminfjones/match-sticks/workflows/Python%20package/badge.svg)

A program that enumerates certain constrained sets of match sticks (edges of
a certain graph on the standard integer lattice points in R^2).


## Description

(This problem was communicated to me by Kyle Ormsby)

The problem is to enumerate all possible configurations of edges between the
integer points of a rectangle in R^2, subject to some mysterious constraints
that arise in homotopy theory.

Consider the 2x2 rectange of integer points with lower left corner at the origin in R^2:

```
*  *  *

*  *  *

*  *  *
```

We're interested in the unit length edges connecting these points (which must
therefor be either vertical or horizontal).

An "Edge Set" in this context is a set of such edges:

```
*--*  *
|
*  *--*

*  *--*
```

We say an edge set is "valid" if three conditions hold:

1. If a vertical edge `v` is in the set, then all the vertical edges to the
   *left* of `v` are also present in the set.
2. Same as (1) with horizontal edges, but replace "left" with "below".
3. Each unit square in the grid must *not* have 3 edges present, i.e. 0, 1, 2,
   and 4 are admissible.

### Examples

The first (emtpy) edge set above is valid in this sense, and the second is
invalid (because there is a horizontal edge in the upper-left with no
horizontal edges below it).

This is also a non-valid edge set: (while attempting to fix the one above by adding
edges below the problematic one, we've made the upper-left square have 3 edges)

```
*--*  *
|
*--*--*

*--*--*
```

And, finally, this is a non-trivial valid edge set:

```
*--*  *
|  |
*--*--*

*--*--*
```

In fact, there are XXX valid edge sets on the 2x2 grid.

### Questions

Given an `n` x `m` rectangle,

1. How many valid edge sets are there?
2. Enumerate all valid edge sets in the rectangle.
3. Exhibit a [generating function](https://en.wikipedia.org/wiki/Generating_function)
   whose coefficients count valid edge sets.
4. Exhibit the number of valid edge sets as a positive sum.


## Installation

This package requires Python 3.7+. The main modules do not have any
requirements beyond the Python standard library. In addition, `pytest` is
required if you want to run tests. We use `flake8` and `mypy` for code
analysis.

To check what python you have, try:

```bash
$ python3 --version
Python 3.7.6
```

To install and run the code in a virtual environment, run the following
commands, assuming your python 3.7+ interpreter is called `python3`:

```bash
$ cd match-sticks
$ python3 -m venv .venv
$ source .venv/bin/activate
$ python3 -m pip install -r requirements.txt
$ python3 -m pip install -e .
```

Now you can run the program:

```bash
$ python3 main.py --help
usage: main.py [-h] [-v] WIDTH HEIGHT

positional arguments:
  WIDTH          width of the grid
  HEIGHT         height of the grid

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  pretty print enumerated edge sets
```

To count (and print) valid edge sets on the 2x1 grid:

```bash
$ python3 main.py --verbose 1 1
Enumerating valid edge sets on 1 x 1 grid

1:
*  *

*  *

2:
*  *

*--*

3:
*  *
|
*  *

4:
*--*

*--*

5:
*  *
|
*--*

6:
*  *
|  |
*  *

7:
*--*
|  |
*--*
```

## Testing and Verification

To test:

```bash
$ python -m pytest
```

To lint/typecheck:

```bash
$ flake8 . --count --show-source --statistics
$ mypy .
```


## TODO

* [X] make initial package commit
* [X] get GitHub CI working
* [X] write a README description of the edge set constraints
* [X] extend validation to include forall unitsquare. (num. edges on unitsquare) != 3
* [X] test `edge_set` validator
* [o] write a recursive enumerator
* [ ] validate results of enumeration using generator function formula
