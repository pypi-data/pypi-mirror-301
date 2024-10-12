"""
Tool to check markers of high-quality projects

This will generate a report of the results of each check. Each check can be
skipped by configuring a `hoptest.toml` file.

For now this supports only Python projects.

Check functions:
These are run by the main function and are conventionally named "check_*".
They should return nothing and raise CheckError if they fail

The `check_security` and `check_code_metrics` functions require that you have
[bandit](https://bandit.readthedocs.io/en/latest/start.html#installation) and
[radon](https://github.com/rubik/radon/tree/master?tab=readme-ov-file#installation)
installed on your system, either in your python virtual environment or globally.
"""

from __future__ import annotations
import os
import subprocess

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
import argparse
from dataclasses import dataclass, field
from typing import List, Optional

try:
    from rich import print
except ImportError:
    pass


COMMIT_MESSAGE_CHECK_RANGE = 3
GITIGNORE_FILE = ".gitignore"
HOPTEST_TOML_PATH = "hoptest.toml"
LICENSE_FILES = [
    "license.txt",
    "License.txt",
    "LICENSE.txt",
    "LICENSE.TXT",
    "LICENSE",
]
PYPROJECT_TOML_PATH = "pyproject.toml"
PROJECT_CONFIG_PATHS = [PYPROJECT_TOML_PATH]
PYTEST_CONFIG_FILE = "conftest.py"
PYTHON_TEST_FILE_PATTERNS = ["**/*test.py", "**/test_*.py"]
SCRIPT_RUNNER_FILES = ["Makefile", "tasks.py"]


class CheckError(Exception):
    """Exception class that is thrown when a check fails, it should contain an error message"""


@dataclass
class HoptestConfig:
    """
    Configuration object for running Hop Test script

    Takes configuration from a toml file
    """

    # used to override default lists
    license_file: Optional[str] = None
    script_runner_file: Optional[str] = None
    project_config_file: Optional[str] = None

    license_files: List[str] = field(init=False, default_factory=lambda: LICENSE_FILES)
    gitignore_file: str = GITIGNORE_FILE
    script_runner_files: List[str] = field(default_factory=lambda: SCRIPT_RUNNER_FILES)
    project_config_files: List[str] = field(
        default_factory=lambda: PROJECT_CONFIG_PATHS
    )
    skip_checks: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.license_file is not None:
            self.license_files = [self.license_file]
        if self.script_runner_file is not None:
            self.script_runner_files = [self.script_runner_file]
        if self.project_config_file is not None:
            self.project_config_files = [self.project_config_file]

    @classmethod
    def from_file(cls, config_file: str) -> HoptestConfig:
        """
        Read a hoptest.toml config file

        Expected to find data under

            [tool.hoptest]
            ...
        """
        # TODO add debug log config file found
        # TODO read from pyproject.toml
        config_data = {}
        if os.path.exists(config_file):
            with open(config_file, mode="rb") as fp:
                config_data = tomllib.load(fp)["tool"]["hoptest"]
        return cls(**config_data)


def commit_message_format(msg: str) -> bool:
    """
    Check that a commit message conforms to a standard format

    The message should be passed a single string with line breaks (if present). The format is:
    - first line is 50 characters or less
    - second line is blank
    - subsequent lines are 72 characters or less
    """
    lines = msg.split("\n")
    if not lines:
        return False
    if len(lines[0]) > 50:
        return False
    second_line = lines[1:2]
    if second_line and len(second_line[0]) > 0:
        return False
    other_lines = lines[2:]
    if other_lines and any(len(line) > 72 for line in other_lines):
        return False
    return True


def check_license(config: HoptestConfig) -> None:
    """Check that a license file exists"""
    for fpath in config.license_files:
        if os.path.exists(fpath):
            return
    # TODO debug log found license file
    raise CheckError(
        "license file not found, if you are using a license file, specify it in hoptest.toml as 'license_file_path'"
    )


def check_gitignore(config: HoptestConfig) -> None:
    """Check that a gitignore file exists"""
    if not os.path.exists(config.gitignore_file):
        raise CheckError(f"gitignore file does not exist at {config.gitignore_file}")


def check_commit_messages(config: HoptestConfig) -> None:
    """Read a few recent commit messages on the main branch and check the format"""
    # TODO debug log commit message if failure
    # for _ in range(COMMIT_MESSAGE_CHECK_RANGE):
    msg = subprocess.check_output(
        ["git", "log", "--format=%B", "--max-count=1"],
        encoding="utf-8",
    )
    if not commit_message_format(msg):
        # TODO link to format
        raise CheckError(
            "the commit message doesn't conform the the standard commit message format"
        )


def check_security(config: HoptestConfig) -> None:
    """Run vulnerability scanners"""
    bandit_args = ["bandit", ".", "-r", "--severity-level", "high"]
    if os.path.exists("pyproject.toml"):
        bandit_args.extend(["-c", "pyproject.toml"])
    ret = subprocess.run(bandit_args, capture_output=True)
    if ret.returncode != 0:
        raise CheckError(
            f"bandit failed, check output by running: {subprocess.list2cmdline(bandit_args)}"
        )


def check_code_metrics(config: HoptestConfig) -> None:
    """
    This checks the 'Maintainability Index' of the code

    See [the radon
    documentation](https://radon.readthedocs.io/en/latest/intro.html#maintainability-index)
    for details and note the caveat.
    """
    radon_mi_args = ["radon", "mi", ".", "--min", "B", "--exclude", "venv/*,.venv/*"]
    ret = subprocess.run(radon_mi_args, capture_output=True)
    if ret.returncode != 0:
        raise CheckError(
            f"radon failed, check output by running: {subprocess.list2cmdline(radon_mi_args)}"
        )


def check_config_files(config: HoptestConfig) -> None:
    """Check that a project config file exists, this can be pyproject.toml"""
    # TODO debug log project config file path
    for config_file_path in config.project_config_files:
        if os.path.exists(config_file_path):
            return
    # TODO better error message
    raise CheckError(
        f"project config file does not exist among {config.project_config_files}"
    )


def check_script_runner(config: HoptestConfig) -> None:
    """Check that a script runner file exists, this can be a Makefile, tasks.py, or similar"""
    for script_runner_file in config.script_runner_files:
        if os.path.exists(script_runner_file):
            return
    # TODO better error message
    raise CheckError(
        f"cannot find project config file among the following: {config.script_runner_files}"
    )


def check_logging(config: HoptestConfig) -> None:
    """Check that we use python's logging module instead of just printing"""
    print_lines = subprocess.run(["git", "grep", "--quiet", "print("], encoding="utf-8")
    logging_lines = subprocess.run(
        ["git", "grep", "--quiet", "logging"], encoding="utf-8"
    )
    print_used = print_lines.returncode == 0
    logging_used = logging_lines.returncode == 0
    if print_used and not logging_used:
        raise CheckError("Using the logging module instead of just `print`")


def check_tests(config: HoptestConfig) -> None:
    """Check that test_*.py or *_test.py files exists, or there is a pytest config file"""
    results = subprocess.check_output(
        ["git", "ls-files", *PYTHON_TEST_FILE_PATTERNS],
        encoding="utf-8",
    )
    # TODO add debug list of results
    if results:
        return
    if os.path.exists(PYTEST_CONFIG_FILE):
        return
    raise CheckError("no python test files")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Hoptest",
        description="Check a repository for markers of high-quality software engineering",
    )
    parser.add_argument(
        "--config",
        type=str,
        help=f"Hoptest configuration file path, default: {HOPTEST_TOML_PATH}",
        default=HOPTEST_TOML_PATH,
    )
    # TODO add arguments to override config file values

    return parser.parse_args()


def main():
    args = parse_args()
    config = HoptestConfig.from_file(args.config)

    checks = [
        check_license,
        check_gitignore,
        check_commit_messages,
        check_security,
        check_code_metrics,
        check_config_files,
        check_script_runner,
        check_logging,
        check_tests,
    ]
    errs = {}
    for check in checks:
        if check.__name__.removeprefix("check_") in config.skip_checks:
            continue
        try:
            check(config)
        except CheckError as err:
            errs[check.__name__] = err
    if errs:
        print("-" * 10)
        for check, err in errs.items():
            print(f"failed check: [bold red]{check}[/bold red]")
            print(f"failure message: {err}")
        print("-" * 10)
    print("Summary")
    print(f"Passed {len(checks)-len(errs)} out of {len(checks)} checks")
    return int(bool(errs))


if __name__ == "__main__":
    main()
