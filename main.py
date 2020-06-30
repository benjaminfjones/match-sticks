"""
Command line program for enumerating valid edge sets.
"""

from enumerate_edge_sets import naively_enumerate_edge_sets
import argparse
import logging


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
        # just print the number without any adornment. Makes the program more unix friendly.
        print(c)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "width",
        type=int,
        metavar="WIDTH",
        help="width of the grid",
    )
    parser.add_argument(
        "height",
        type=int,
        metavar="HEIGHT",
        help="height of the grid",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="pretty print enumerated edge sets",
    )
    parser.add_argument(
        "--profile",
        action="store_true",
        help="dump profiler statistics",
    )
    parser.add_argument(
        "--loglevel",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        metavar="LEVEL",
        default="WARNING",
        help="logging level to emit: DEBUG, INFO, WARNING (default), ERROR",
    )

    args = parser.parse_args()

    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)
    logging.basicConfig(level=numeric_level, format='%(levelname)s:%(message)s')

    if args.height < 0 or args.width < 0:
        raise ValueError(f"Height ({args.height}) and width ({args.width}) must be non-negative!")

    logging.info(f"Enumerating valid edge sets on {args.width} x {args.height} grid")

    if args.profile:
        logging.info("Starting cProfile...")
        import cProfile
        cProfile.runctx("run_enumeration(args)", globals(), locals())
    else:
        run_enumeration(args)


if __name__ == '__main__':
    main()
