import argparse
import logging
import os

import ghm.meta as meta


def parse():
    parser = argparse.ArgumentParser(
        prog=meta.NAME,
        description=meta.DESCRIPTION,
        epilog=f"{meta.COPYRIGHT} ({meta.URL})",
        # FIXME: https://bugs.python.org/issue27927
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{meta.NAME} {meta.VERSION}"
    )
    parser.add_argument(
        "-t",
        "--token",
        default=os.environ.get("GH_TOKEN", os.environ.get("GITHUB_TOKEN")),
        help="github access token"
    )
    parser.add_argument(
        "-u",
        "--user",
        help="mirror a specific user's repositories"
    )
    parser.add_argument(
        "-o",
        "--org",
        help="mirror a specific organization's repositories"
    )
    parser.add_argument(
        "--owner",
        help="filter repositories by owner"
    )
    parser.add_argument(
        "--repo",
        help="filter repositories by name"
    )
    parser.add_argument(
        "--exclude-owner"
    )
    parser.add_argument(
        "--exclude-repo"
    )
    parser.add_argument(
        "--exclude-forks",
        action="store_true",
        help="exclude forks"
    )
    parser.add_argument(
        "--threads",
        default=os.cpu_count(),
        help="number of threads to run"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what will happen without making changes"
    )
    parser.add_argument(
        "-l",
        "--log-level",
        choices=("debug", "info", "warning", "error", "critical"),
        default="info",
        help="show messages of this level or higher"
    )
    parser.add_argument(
        "path",
        help="local path"
    )

    options = parser.parse_args()

    if options.dry_run:
        log_format = "[%(levelname)s] (DRY-RUN) %(message)s"
    else:
        log_format = "[%(levelname)s] %(message)s"

    log_level = getattr(logging, options.log_level.upper())
    logging.basicConfig(format=log_format, level=log_level)

    return options
