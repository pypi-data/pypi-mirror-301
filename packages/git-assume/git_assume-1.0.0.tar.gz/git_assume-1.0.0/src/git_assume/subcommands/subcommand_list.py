import argparse
import logging
import os
from logging import Logger, getLogger

from .. import utils


def validate_list_args(args: argparse.ArgumentParser, logger: Logger):
    # validate netrc-longterm file
    if not os.path.isfile(args.netrc_longterm):
        raise FileNotFoundError(f"{args.netrc_longterm} does not exist.")
    logger.debug(f"Found .netrc-longterm: {args.netrc_longterm}")


def gitassume_list(args: argparse.ArgumentParser):
    logger = getLogger(__name__)
    logger.setLevel(getattr(logging, args.log_level))

    validate_list_args(args, logger)

    netrc_longterm_config = utils.read_netrc_longterm(args.netrc_longterm, logger)
    utils.validate_netrc_longterm_config(netrc_longterm_config, profile=None, logger=logger)
    print(f"Profiles that exist in .netrc-longterm: {args.netrc_longterm}")
    for section in netrc_longterm_config.sections():
        print(f"- {section}")
