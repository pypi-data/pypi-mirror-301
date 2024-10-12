from .aws.plugins import (
    MotoPlugin,
)
from .plugins import (
    CustomFixturesPlugin,
)
import argparse
import coverage
import pathlib
from pathlib import (
    Path,
)
import pytest
import sys
from typing import (
    NamedTuple,
)


class Args(NamedTuple):
    target: pathlib.Path
    scope: str


def _get_args() -> Args:
    parser = argparse.ArgumentParser(
        prog="fluidattacks_core.testing",
        description=(
            "🏹 Python package for unit and integration testing through "
            "Fluid Attacks projects 🏹"
        ),
    )

    parser.add_argument(
        "--target",
        metavar="TARGET",
        type=pathlib.Path,
        required=True,
        help="Directory to start the tests. Default is current directory.",
    )

    parser.add_argument(
        "--scope",
        metavar="SCOPE",
        type=str,
        required=True,
        help="Type and module to test.",
    )

    args = parser.parse_args()

    return Args(
        target=args.target,
        scope=args.scope,
    )


def _cov_init(args: Args) -> coverage.Coverage:
    cov = coverage.Coverage()
    cov.set_option("run:source", [f"{args.target}/{args.scope}"])
    cov.set_option("run:include", [f"{args.target}/{args.scope}/*"])
    cov.set_option("run:branch", True)

    return cov


def _cov_read(cov_path: Path) -> float:
    if cov_path.is_file():
        with open(cov_path, "r", encoding="utf-8") as cov_file:
            return float(cov_file.read())
    return 0.0


def _cov_write(cov_path: Path, cov: float) -> None:
    if not cov_path.is_file():
        cov_path.touch()
    with open(cov_path, "w", encoding="utf-8") as cov_file:
        cov_file.write(str(cov))


def _cov_test(args: Args, cov: coverage.Coverage) -> bool:
    path = Path(f"{args.target}/{args.scope}/coverage")
    current = _cov_read(path)
    new = cov.report(
        output_format="text",
        skip_covered=True,
        skip_empty=True,
        sort="cover",
    )

    if new == current:
        print(f"Coverage did not change from {current}.")
        return True
    if new > current:
        print(
            f"Coverage increased from {current} to {new}. "
            "Please add new coverage to your commit."
        )
        _cov_write(path, new)
        return False
    print(f"Coverage decreased from {current} to {new}. Please add tests.")
    return False


def _pytest(args: Args) -> bool:
    pytest_args = [
        "--disable-warnings",
        "--showlocals",
        "--strict-markers",
        "--verbose",
        "-m",
        args.scope,
    ]
    exit_code = pytest.main(
        [str(args.target), *pytest_args],
        plugins=[
            CustomFixturesPlugin(),
            MotoPlugin(),
        ],
    )
    return exit_code == 0


def main() -> bool:
    args = _get_args()
    cov = _cov_init(args)
    cov.start()

    pytest_result = _pytest(args)

    cov.stop()
    cov_result = _cov_test(args, cov)

    result = pytest_result and cov_result

    return sys.exit(0) if result else sys.exit(1)
