"""
Command line program for enumerating valid edge sets.
"""

from enumerate_edge_sets import enumerate_edge_sets
import argparse


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
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="pretty print enumerated edge sets"
    )

    args = parser.parse_args()

    if args.height < 0 or args.width < 0:
        raise ValueError(f"Height ({args.height}) and width ({args.width}) must be non-negative!")

    if args.verbose:
        print(f"Enumerating valid edge sets on {args.height} x {args.width} grid")

    c = 1  # we're counting like mathematicians
    for es in enumerate_edge_sets(args.height, args.width):
        if args.verbose:
            print(f"\n{c}:\n" + es.pretty_print())
        c = c + 1

    if not args.verbose:
        print(f"Number of valid edge sets: {c}")


if __name__ == '__main__':
    main()
