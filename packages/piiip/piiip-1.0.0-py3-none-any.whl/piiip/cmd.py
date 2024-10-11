from __future__ import annotations

import argparse
import logging
import shutil
import subprocess
import sys
import threading
from multiprocessing import Queue
from typing import Sequence

from piiip._logger import logger
from piiip.cache import Cache
from piiip.intended_name_generator import IntendedNameGenerator
from piiip.package import Package

PYPI_PROTO = "https"
PYPI_FQDN = "pypi.org"
PYPI_PACKAGE_INDEX = "simple"
PIP_INSTALL_OPTIONS_NO_ARGS = [
    "-U",
    "--upgrade",
    "--force-reinstall",
    "-I",
    "--ignore-installed",
    "--no-deps",
    "--user",
    "--egg",
    "--compile",
    "--no-compile",
    "--no-use-wheel",
    "--pre",
    "--no-clean",
    "--dry-run",
    "--ignore-requires-python",
    "--no-build-isolation",
    "--use-pep517",
    "--check-build-dependencies",
    "--break-system-packages",
    "--no-warn-script-location",
    "--no-warn-conflicts",
    "--prefer-binary",
    "--require-hashes",
]
PIP_INSTALL_OPTIONS_ONE_ARG = [
    "-e",
    "--editable",
    "-b",
    "--build",
    "-t",
    "--target",
    "-d",
    "--download",
    "--download-cache",
    "--src",
    "--root",
    "-c",
    "--constraint",
    "--platform",
    "--python-version",
    "--implementation",
    "--abi",
    "--prefix",
    "--upgrade-strategy",
    "-C",
    "--config-settings",
    "--global-option",
    "--no-binary",
    "--only-binary",
    "--progress-bar",
    "--root-user-action",
    "--report",
]
PIP_UNSUPPORTED_OPTIONS = [
    ".",
    "-i",
    "--index-url",
    "--extra-index-url",
    "--no-index",
    "-f",
    "--find-links",
    "-r",
    "--requirement",
]
PIP_INSTALL_OPTIONS_MULTI_ARGS = ["--install-option", "--global-option"]
PIIIP_DESCRIPTION = """piiip (Piiip Interactively Installs Intended Packages) is a wrapper around pip that helps to avoid installation of a different package than was intended. For example, when executing piiip install panddas (panddas instead of pandas), piiip asks for a confirmation before commencing the installation of panddas. piiip is a drop-in replacement for pip; usage is exactly equal."""
PIIIP_HELP_MESSAGE = (
    """usage: piiip [-h] [-v] install [pip options] package

"""
    + PIIIP_DESCRIPTION
    + """

options:
  -h, --help         show this help message and exit
  --verbose, -v      enable verbose logging (can also be specified through `piiip_V`)
  --dry-run DRY_RUN  run piiip but do not actually install packages


pip"""
)
RED_TERMINAL_CHARS = "\x1b[31;20m"
NORMAL_TERMINAL_CHARS = "\x1b[0m"


class CMD:

    def __init__(self, verbose: bool = False) -> None:
        if verbose:
            logger.setLevel(logging.DEBUG)
        self.all_pypi_packages = self.get_all_pypi_packages_from_file(
            PYPI_PROTO, PYPI_FQDN, PYPI_PACKAGE_INDEX
        )

    def handle_input(
        self, parsed: argparse.Namespace, args: list[str] | None = None
    ) -> None:
        arguments = args if args is not None else sys.argv[1:]
        to_be_checked_packages = self.get_to_be_installed_package_names(arguments)
        to_be_checked_packages_equalized = []
        for package in to_be_checked_packages:
            equalized_package = self.equalize_package_name(package)
            to_be_checked_packages_equalized.append(equalized_package)
        self.ask_installing_possibly_unintended_packages(
            to_be_checked_packages_equalized
        )
        code = 0
        if parsed.dry_run:
            logger.info(f"This is a dry run, nothing is installed")
            self.quit(code)
        else:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", _get_pip_installer()] + arguments
                )
            except subprocess.CalledProcessError as exc:
                code = exc.returncode
        self.quit(code)

    def ask_installing_possibly_unintended_packages(
        self, packages: Sequence[str]
    ) -> None:
        for package in packages:
            if not self.safety_check(package):
                response = input()
                if response in ["y", "Y", "yes"]:
                    continue
                else:
                    logger.info("Not installing packages, aborting")
                    self.quit()

    def get_to_be_installed_package_names(self, arguments: Sequence[str]) -> list[str]:
        install_identified = False
        package_names: list[str] = []
        ignore_next_command_part = False
        for command_part in arguments:
            if install_identified:
                if command_part in PIP_UNSUPPORTED_OPTIONS:
                    logger.error(
                        "piiip: currently installation sources other than pypi.org are not supported by piiip. Please use pip instead. Would you like this option supported by piiip? Consider opening an issue at https://github.com/TNO-S3/piiip. Aborting."
                    )
                    self.quit()
                if ignore_next_command_part:
                    ignore_next_command_part = False
                    continue
                if command_part in PIP_INSTALL_OPTIONS_NO_ARGS:
                    continue  # ignore an option to pip install
                if command_part in PIP_INSTALL_OPTIONS_ONE_ARG:
                    ignore_next_command_part = True
                    continue  # ignore an option to pip install and its argument
                if command_part in PIP_INSTALL_OPTIONS_MULTI_ARGS:
                    logger.error(
                        "piiip: pip install options --install-option and --global-option are not supported in piiip. Please use pip instead. Aborting."
                    )
                    self.quit()
                if (
                    command_part[:1] == "-"
                ):  # this works as PyPi packages have to start with a letter or a number https://peps.python.org/pep-0508/#names
                    return package_names
            if install_identified:
                package_names.append(command_part)
            if command_part == "install":
                install_identified = True
        return package_names

    def safety_check(self, package_name: str) -> bool:
        """
        Checks whether the package name might contain a typo.
        If so, asks whether to proceed and exits the program if
        proceeding is not desired. In all other cases, returns
        control to PIP.
        Returns True if installing is deemed safe, False otherwise.
        """
        if not self.package_exists(package_name):
            logger.info(f"piiip: package {package_name} does not exist")
            return True
        package = Package(package_name)
        possibly_intended_packages = self.get_possibly_intended_packages(package.name)
        possibly_intended_packages = sorted(
            possibly_intended_packages,
            key=lambda package: package.popularity,
            reverse=True,
        )
        # Filter out all packages that are less popular than the target package
        possibly_intended_packages = [
            p for p in possibly_intended_packages if p.popularity > package.popularity
        ]
        if len(possibly_intended_packages) == 0:
            return True
        if len(possibly_intended_packages) == 1:
            logger.info(
                f"A package named {RED_TERMINAL_CHARS}{possibly_intended_packages[0].name}{NORMAL_TERMINAL_CHARS} instead of {RED_TERMINAL_CHARS}{package.name}{NORMAL_TERMINAL_CHARS} exists. Are you sure you want to install {RED_TERMINAL_CHARS}{package.name}{NORMAL_TERMINAL_CHARS}? (y/n)"
            )
            return False
        if len(possibly_intended_packages) > 1:
            package_list_str = ""
            for i, pkg in enumerate(possibly_intended_packages):
                if i == 0:
                    package_list_str += (
                        f"{RED_TERMINAL_CHARS}{pkg.name}{NORMAL_TERMINAL_CHARS}"
                    )
                else:
                    package_list_str += (
                        f" and {RED_TERMINAL_CHARS}{pkg.name}{NORMAL_TERMINAL_CHARS}"
                    )
            logger.info(
                f"Packages named {package_list_str} instead of {RED_TERMINAL_CHARS}{package.name}{NORMAL_TERMINAL_CHARS} exists. Are you sure you want to install {RED_TERMINAL_CHARS}{package.name}{NORMAL_TERMINAL_CHARS}? (y/n)"
            )
        return False

    def package_exists(self, package_name: str) -> bool:
        """
        Verifies whether a package exists. Returns True if the package
        exists, False otherwise.
        """
        return package_name in self.all_pypi_packages

    def get_all_pypi_packages_from_file(
        self, protocol: str, FQDN: str, file_path: str
    ) -> set[str]:
        all_names = set()
        cache_file = Cache().get_file(protocol, FQDN, file_path)
        with open(cache_file) as f:
            for line in f:
                if line.strip()[:8] != "<a href=":
                    continue
                package_name = line.strip().split(  # for every line  # remove leading and trailing whitespace
                    '/">'
                )[  # split the line in before and after '/">"
                    -1
                ][  # take the last part (after '/">')
                    :-4
                ]  # remove the last four characters
                package_name = self.equalize_package_name(package_name)
                if line.strip()[17 : 17 + len(package_name)] != package_name:
                    raise ValueError(
                        f"Extracting the name of package {package_name} went wrong"
                    )
                all_names.add(package_name)
        if len(all_names) < 500000 or "charset-normalizer" not in all_names:
            raise ValueError("Parsing list of all Pypi packages went wrong")
        return all_names

    def equalize_package_name(self, package_name: str) -> str:
        """
        "Comparison of project names is case insensitive and treats arbitrarily
        long runs of underscores, hyphens, and/or periods as equal" https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#writing-pyproject-toml
        All package names are made lower case and (sequences of) underscores, hyphens, and periods
        are converted to single hyphens (as pypi does itself in the url to a package).
        """
        package_name = package_name.lower()
        package_name = package_name.replace(".", "-")
        package_name = package_name.replace("_", "-")
        while "--" in package_name:
            package_name = package_name.replace("--", "-")
        return package_name

    def get_possibly_intended_packages(self, package_name: str) -> list[Package]:
        """
        Tries to access whether the given package name was intended
        or might be wrong. Returns True if there is a chance the name
        is wrong, False if the name is likely right.
        """
        logger.debug("Getting possibly intended packages")
        candidate_names = IntendedNameGenerator().generate_possibly_intended_names(
            package_name
        )
        existing_candidate_names = set()
        for candidate_name in candidate_names:
            if self.package_exists(candidate_name):
                existing_candidate_names.add(candidate_name)
        logger.debug(
            f"Number of generated names that exists: {len(existing_candidate_names)}"
        )
        candidates = self.initialize_candidates_parallel(existing_candidate_names)
        return self.more_popular_candidates(package_name, candidates)

    def initialize_candidates_parallel(
        self, existing_candidate_names: set[str]
    ) -> list[Package]:
        candidate_queues = []
        candidate_creating_threads = []
        for candidate_name in existing_candidate_names:
            q: Queue[Package | Exception] = Queue()
            t = threading.Thread(
                target=self.initialize_candidate, args=(candidate_name, q)
            )
            t.start()
            candidate_queues.append(q)
            candidate_creating_threads.append(t)
        for t in candidate_creating_threads:
            t.join()
        candidates = []
        for q in candidate_queues:
            candidate = q.get()
            if isinstance(candidate, Exception):
                raise ValueError(candidate)
            candidates.append(candidate)
        return candidates

    def initialize_candidate(
        self, candidate_name: str, queue: Queue[Package | Exception]
    ) -> None:
        try:
            p = Package(candidate_name)
            queue.put(p)
        except Exception as E:
            queue.put(E)

    def more_popular_candidates(
        self, package_name: str, candidates: list[Package]
    ) -> list[Package]:
        """
        Returns a list of all candidate packages in candidates that are more popular than package_name
        """
        target_package = Package(package_name)
        more_popular_candidates = []
        for candidate in candidates:
            if target_package.popularity < candidate.popularity:
                more_popular_candidates.append(candidate)
        return more_popular_candidates

    def quit(self, code: int = 0) -> None:
        Cache().save_cache_to_disk()
        exit(code)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=PIIIP_DESCRIPTION,
        usage="piiip [-h] [-v] install [pip options] package",
        epilog="All other arguments are passed directly to pip.",
        add_help=False,
    )
    parser.add_argument(
        "--verbose",
        "-v",
        help="enable verbose logging (can also be specified through `PIIIP_V`)",
        action="count",
    )
    parser.add_argument(
        "--dry-run",
        help="run piiip but do not actually install packages",
        action="store_true",
    )
    parser.add_argument(
        "--help",
        "-h",
        help="display help",
        action="store_true",
    )
    args, non_parsed = parser.parse_known_args()
    if args.verbose:
        non_parsed.extend(["--verbose"] * args.verbose)
        args.verbose = True
    if args.help or len(sys.argv) <= 1:
        print(PIIIP_HELP_MESSAGE)
        non_parsed.extend(["--help"] * args.help)
    CMD(args.verbose).handle_input(args, non_parsed)


def _get_pip_installer() -> str:
    _PIP_INSTALLERS = ["pip", "pip3"]
    try:
        return next(filter(_is_executable, _PIP_INSTALLERS))
    except StopIteration:
        raise SystemError("Could not determine pip installer executable")


def _is_executable(name: str) -> bool:
    """
    Check whether the provided name is an executable.
    """
    return shutil.which(name) is not None


if __name__ == "__main__":
    main()
