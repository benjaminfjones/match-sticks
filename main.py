"""
Command line program for enumerating valid edge sets.
"""

from enumerate_edge_sets import naively_enumerate_edge_sets
import argparse


def run_enumeration(args):
    # TODO replace naive version with recursive version
    valid_edge_sets = naively_enumerate_edge_sets(args.width, args.height)

    if args.verbose:
        c = 0
        for es in valid_edge_sets:
            c = c + 1  # count like a mathematician
            print(f"\n{c}:\n" + es.pretty_print())
    else:
        c = len(list(valid_edge_sets))
        print(f"Number of valid edge sets: {c}")


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
    parser.add_argument(
        "--profile",
        action="store_true",
        help="dump profiler statistics"
    )

    args = parser.parse_args()

    if args.height < 0 or args.width < 0:
        raise ValueError(f"Height ({args.height}) and width ({args.width}) must be non-negative!")

    if args.verbose:
        print(f"Enumerating valid edge sets on {args.width} x {args.height} grid")

    if args.profile:
        import cProfile
        cProfile.runctx("run_enumeration(args)", globals(), locals())
    else:
        run_enumeration(args)


if __name__ == '__main__':
    main()
