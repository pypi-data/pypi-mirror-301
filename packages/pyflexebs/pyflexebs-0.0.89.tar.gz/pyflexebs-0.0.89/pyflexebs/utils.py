import logging
import os
import sys
from subprocess import Popen, PIPE

import pypathutil.common

import pyflexebs
from pyflexebs.configs import ConfigProxy


def run_with_logger(args, logger):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    logger.info(f"running [{','.join(args)}]")
    with Popen(args, stdout=PIPE, stderr=PIPE) as proc:
        out, err = proc.communicate()
        exitcode = proc.returncode
    if exitcode != 0:
        logger.error(f"error in execution with code [{exitcode}]")
        logger.debug(f"stdout was [{out.decode()}]")
        logger.debug(f"stderr was [{err.decode()}]")
    else:
        logger.info("execution was successful")


def get_logger():
    return logging.getLogger(pyflexebs.LOGGER_NAME)


def check_root():
    if not os.geteuid() == 0:
        sys.exit('Script must be run as root')


def configure_proxy():
    if ConfigProxy.http_proxy is not None:
        os.environ['http_proxy'] = ConfigProxy.http_proxy
        os.environ['HTTP_PROXY'] = ConfigProxy.http_proxy
    if ConfigProxy.https_proxy is not None:
        os.environ['https_proxy'] = ConfigProxy.https_proxy
        os.environ['HTTPS_PROXY'] = ConfigProxy.https_proxy
    if ConfigProxy.no_proxy is not None:
        os.environ['no_proxy'] = ConfigProxy.no_proxy
        os.environ['NO_PROXY'] = ConfigProxy.no_proxy


def check_tools():
    """
    Check that the command line tools we need are available
    """
    logger = get_logger()
    problems = False
    for app in ["xfs_growfs", "resize2fs"]:
        if pypathutil.common.find_in_standard_path(app) is None:
            problems = True
            logger.error(f"please install executable [{app}]")
    if problems:
        sys.exit(1)


def dump(obj):
    """
    debugging function to dump objects
    """
    for attr in dir(obj):
        if attr.startswith("__"):
            continue
        print(f"obj.{attr} = {getattr(obj, attr)}")
