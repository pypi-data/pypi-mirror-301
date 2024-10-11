import argparse
import os
from typing import List, Optional

from git_assume import utils

from .subcommands.subcommand_assume import gitassume_assume
from .subcommands.subcommand_list import gitassume_list

LOGGER_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "logger_config.yml"))

DEFAULT_NETRC_SHORTTERM_PATH = f"{os.path.expanduser('~')}/.netrc"
DEFAULT_NETRC_LONGTERM_PATH = f"{os.path.expanduser('~')}/.netrc-longterm"


def main(argv: Optional[List] = None):
    utils.setup_logger(LOGGER_CONFIG_PATH)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_assume = subparsers.add_parser("assume", help="see `assume -h`")
    parser_assume.add_argument("profile", nargs="?", default="default")
    parser_assume.add_argument(
        "--netrc-longterm", required=False, default=DEFAULT_NETRC_LONGTERM_PATH
    )
    parser_assume.add_argument("--netrc", required=False, default=DEFAULT_NETRC_SHORTTERM_PATH)
    parser_assume.add_argument(
        "--log-level",
        help="Set log level",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
        required=False,
        default="INFO",
    )
    parser_assume.add_argument("-y", "--yes", required=False, action="store_true")
    parser_assume.set_defaults(handler=gitassume_assume)

    parser_assume = subparsers.add_parser("list", help="see `list -h`")
    parser_assume.add_argument(
        "--netrc-longterm", required=False, default=DEFAULT_NETRC_LONGTERM_PATH
    )
    parser_assume.add_argument(
        "--log-level",
        help="Set log level",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
        required=False,
        default="INFO",
    )
    parser_assume.set_defaults(handler=gitassume_list)

    if argv is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(argv)

    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
