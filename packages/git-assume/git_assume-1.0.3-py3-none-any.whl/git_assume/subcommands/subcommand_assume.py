import argparse
import logging
import os
import sys
from logging import Logger, getLogger

from .. import utils


def validate_assume_args(args: argparse.ArgumentParser, logger: Logger):
    # validate netrc file
    if not os.path.isfile(args.netrc):
        raise FileNotFoundError(f"{args.netrc} does not exist.")
    logger.debug(f"Found .netrc: {args.netrc}")

    # validate netrc-longterm file
    if not os.path.isfile(args.netrc_longterm):
        raise FileNotFoundError(f"{args.netrc_longterm} does not exist.")
    logger.debug(f"Found .netrc-longterm: {args.netrc_longterm}")


def gitassume_assume(args: argparse.ArgumentParser):
    logger = getLogger(__name__)
    logger.setLevel(getattr(logging, args.log_level))

    validate_assume_args(args, logger)

    netrc_longterm_config = utils.read_netrc_longterm(args.netrc_longterm, logger)
    utils.validate_netrc_longterm_config(netrc_longterm_config, profile=args.profile, logger=logger)

    curr_netrc = utils.read_netrc(args.netrc, logger)
    logger.debug(f"Successfully read .netrc: {args.netrc}")
    logger.debug("current .netrc setting:")
    for key, value in curr_netrc.items():
        logger.debug(f"  {key} = {value}")

    while not args.yes:
        ans = utils.ask(f"Are you sure to overwrite {args.netrc} with profile `{args.profile}`??")
        if ans is None:
            continue
        if not ans:
            logger.info(f"No update on {args.netrc}")
            sys.exit(0)
        elif ans:
            break

    utils.write_netrc(netrc_longterm_config[args.profile], args.netrc, logger)
