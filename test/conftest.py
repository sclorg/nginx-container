import os
import sys

from pathlib import Path
from collections import namedtuple
from pytest import skip

from container_ci_suite.utils import check_variables

if not check_variables():
    sys.exit(1)

TAGS = {
    "rhel8": "-ubi8",
    "rhel9": "-ubi9",
    "rhel10": "-ubi10",
}

Vars = namedtuple(
    "Vars", [
        "OS", "TAG", "VERSION", "IMAGE_NAME", "VERSION_NO_MICRO", "SHORT_VERSION", "TEST_DIR"
    ]
)
OS = os.getenv("TARGET").lower()
VERSION = os.getenv("VERSION")
BRANCH_TO_TEST = "master"

VARS = Vars(
    OS=OS,
    TAG=TAGS.get(OS),
    VERSION=VERSION,
    IMAGE_NAME=os.getenv("IMAGE_NAME"),
    VERSION_NO_MICRO=VERSION.replace("-micro", ""),
    SHORT_VERSION=VERSION.replace("-micro", "").replace(".", ""),
    TEST_DIR=Path(__file__).parent.absolute(),
)


def skip_clear_env_tests():
    if VARS.OS == "rhel8" and VERSION == "8.2":
        skip(f"Skipping clear env tests for {VARS.VERSION} on {VARS.OS}.")
