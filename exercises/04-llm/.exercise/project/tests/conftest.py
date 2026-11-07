"""What your tests can use: the card, the evidence files, and two helpers. Pick the card with CARD=path."""
import os
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_FILES = ["metrics.json", "params.yaml", "release.yaml", "sources.yaml"]


@pytest.fixture
def card():
    """The text of the card named by the CARD environment variable."""
    return Path(os.environ["CARD"]).read_text()


@pytest.fixture
def evidence():
    """The text of the files a card's numbers and URLs may come from."""
    return "\n".join((ROOT / name).read_text() for name in EVIDENCE_FILES)


@pytest.fixture
def numbers():
    """A function: the set of numbers in a text, leaving out URLs, versions, DOIs and `code`."""

    def find(text):
        text = re.sub(r"https?://\S+", " ", text)
        text = re.sub(r"\bv\d+\.\d+\.\d+\b", " ", text)
        text = re.sub(r"10\.\d{4,}/\S+", " ", text)
        text = re.sub(r"`[^`]*`", " ", text)
        return set(re.findall(r"(?<![\w.])\d+(?:\.\d+)?(?![\w]|\.\d)", text))

    return find


@pytest.fixture
def urls():
    """A function: the set of URLs in a text."""

    def find(text):
        return {url.rstrip(").,>]*`") for url in re.findall(r"https?://[^\s)\]>`]+", text)}

    return find
