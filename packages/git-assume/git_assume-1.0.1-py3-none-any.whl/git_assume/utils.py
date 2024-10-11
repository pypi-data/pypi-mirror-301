import configparser
import logging
import logging.config
import sys
from logging import Logger
from typing import Dict, Optional

import yaml


def ask(question: str, include_guide: bool = True) -> Optional[bool]:
    dic = {"": True, "y": True, "yes": True, "n": False, "no": False}
    if include_guide:
        question += " [Y/n] "
    ans = input(question).lower()
    return dic.get(ans, None)


def setup_logger(logger_configfile_path: str):
    with open(logger_configfile_path, "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)


def validate_netrc_longterm_config(
    netrc_longterm_config: configparser.ConfigParser, logger: Logger, profile: Optional[str] = None
):
    if profile is not None and profile not in netrc_longterm_config:
        raise KeyError(f"Expected profile `{profile}` does not exist.")

    required_attributes = ("machine", "login", "password")
    for section in netrc_longterm_config.sections():
        for attr in required_attributes:
            if (
                attr not in netrc_longterm_config[section]
                or netrc_longterm_config[section][attr] == ""
            ):
                raise KeyError(f"Attribute `{attr}` does not exist in profile `{profile}`")

    logger.debug("Config file validation finished. " "All required attributes exist.")


def read_netrc(filename: str, logger: Logger) -> Dict[str, str]:
    with open(filename, "r") as f:
        ret = {}
        for line in f:
            line = line.strip()
            # ignore blank lines and comments
            if line == "" or line.startswith("#"):
                continue
            elements = [elem for elem in line.split(" ") if not elem.startswith("#")]

            if len(elements) != 2:
                raise Exception(f"File format invalid. Each line of {filename} must be 2.")

            ret[elements[0].strip()] = elements[1].strip()
    return ret


def write_netrc(netrc: Dict[str, str], filename: str, logger: Logger):
    with open(filename, "w") as f:
        for key, value in netrc.items():
            f.write(f"{key} {value}\n")
            logger.debug(f"Successfully write: {key} = {value}")
    logger.info(f"Successfully write to .netrc: {filename}")


def read_netrc_longterm(filename: str, logger: Logger) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    try:
        config.read(filename)
    except configparser.ParsingError:
        logger.error(f"Can't parse {filename}")
        sys.exit(1)

    logger.debug(f"Successfully parsed {filename}")
    return config
