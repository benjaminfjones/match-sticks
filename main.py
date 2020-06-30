"""
Command line program for enumerating valid edge sets.
"""

from enumerate_edge_sets import naively_enumerate_edge_sets
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "width",
        type=int,
        metavar="WIDTH",
        help="width of the grid"
    )
    parser.add_argument(
        "height",
        type=int,
        metavar="HEIGHT",
        help="height of the grid"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="pretty print enumerated edge sets"
    )

    args = parser.parse_args()

    if args.height < 0 or args.width < 0:
        raise ValueError(f"Height ({args.height}) and width ({args.width}) must be non-negative!")

    if args.verbose:
        print(f"Enumerating valid edge sets on {args.width} x {args.height} grid")

    c = 0
    # TODO replace naive version with recursive version
    for es in naively_enumerate_edge_sets(args.width, args.height):
        c = c + 1  # count like a mathematician
        if args.verbose:
            print(f"\n{c}:\n" + es.pretty_print())

    if not args.verbose:
        print(f"Number of valid edge sets: {c}")


if __name__ == '__main__':
    main()
