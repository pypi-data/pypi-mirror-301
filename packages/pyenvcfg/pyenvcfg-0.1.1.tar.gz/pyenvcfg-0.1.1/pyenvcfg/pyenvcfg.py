#!/usr/bin/env python

"""pyenvcfg to init envcfg setup"""

import logging
import os

import click
import git
from jcgutier_logger.logger import Logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# click cli to call module
@click.group()
@click.option("--debug", is_flag=True, help="Enable debug logs")
def cli(debug=False):
    """Cli command group

    Args:
        debug (bool, optional): To show debug logs. Defaults to False.
    """
    Logger(debug)


@cli.command()
def install():
    """Install pyenvcfg"""
    logger.debug("Installing pyenvcfg...")

    # Create directory to clone envcfg repository
    envcfg_dir = f"{os.getenv('HOME')}/github.com/jcgutier/"
    logger.debug("Creating directory for envcfg: %s", envcfg_dir)
    os.makedirs(envcfg_dir, exist_ok=True)

    # Clone envcfg repository
    envcfg_repo = "https://gitlab.com/jcgutier/jcgutier"
    logger.debug(
        "Cloning envcfg repo: %s, on directory: %s",
        envcfg_repo,
        envcfg_dir,
    )
    try:
        git.Repo.clone_from(envcfg_repo, envcfg_dir)
        logger.debug("Repo cloned")
        click.secho("Envcfg repo cloned", fg="green")
    except git.exc.GitError:
        logger.debug(
            "Can not clone as the directory is not empty. Trying to update"
        )
        repo = git.Repo(f"{envcfg_dir}/envcfg")
        repo.remotes.origin.pull()
        logger.debug("Repo updated")
        click.secho("Envcfg repo updated", fg="green")


if __name__ == "__main__":
    cli()
