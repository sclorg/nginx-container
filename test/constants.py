import os
from pathlib import Path

TAGS = {
    "rhel8": "-ubi8",
    "rhel9": "-ubi9",
    "rhel10": "-ubi10",
}

VERSION = os.getenv("VERSION")
OS = os.getenv("OS").lower()
IMAGE_NAME = os.getenv("IMAGE_NAME")
TEST_DIR = Path(__file__).parent.absolute()
