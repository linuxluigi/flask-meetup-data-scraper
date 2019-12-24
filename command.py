import argparse
from meetup_search.commands.get_groups import GetGroups


def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser("meetup-search")

    parser.add_argument("get_groups", help="load all groups JSONs")

    return parser


def main(args=None):
    """
    Main entry point
    Args:
        args : list
            A of arguments as if they were input in the command line. Leave it
            None to use sys.argv.
    """

    parser = get_parser()
    args = parser.parse_args(args)

    # load config
    # conf = read_config.main(args.config_path)

    if args.get_groups:
        return GetGroups()


if __name__ == "__main__":
    main()
