import os
import pytest


def get_data_filecontent(filename: str) -> str:
    """
    Read content of a file in the data directory.

    Args:
        filename: str: file to read

    Returns:
        File content

    """
    fullpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "data", filename
    )
    with open(fullpath) as f:
        return f.read()


def parse_motslettres_txt(filename: str) -> list[str]:
    """
    Read file in data directory and extract word list from it.
    The file is expected to be in the data directory, and contain one word per line.

    Args:
        filename: str: file to read

    Returns:
        Word list
    """
    content = get_data_filecontent(filename)
    return [word for word in content.split("\n") if word != ""]


@pytest.fixture(scope="session")
def mots4lettrespage1_html() -> str:
    return get_data_filecontent("mots4lettrespage1.html")


@pytest.fixture(scope="session")
def mots4lettrespage2_html() -> str:
    return get_data_filecontent("mots4lettrespage2.html")


@pytest.fixture(scope="session")
def mots4lettrespage3_html() -> str:
    return get_data_filecontent("mots4lettrespage3.html")


@pytest.fixture(scope="session")
def mots4lettrespage4_html() -> str:
    return get_data_filecontent("mots4lettrespage4.html")


@pytest.fixture(scope="session")
def mots4lettrespage5_html() -> str:
    return get_data_filecontent("mots4lettrespage5.html")


@pytest.fixture(scope="session")
def mots6lettrespage1_html() -> str:
    return get_data_filecontent("mots6lettrespage1.html")


@pytest.fixture(scope="session")
def mots8lettrespage1_html() -> str:
    return get_data_filecontent("mots8lettrespage1.html")


@pytest.fixture(scope="session")
def allmots4lettres() -> list[str]:
    return parse_motslettres_txt("allmots4lettres.txt")


@pytest.fixture(scope="session")
def mots6lettrespage1() -> list[str]:
    return parse_motslettres_txt("mots6lettrespage1.txt")


@pytest.fixture(scope="session")
def mots8lettrespage1() -> list[str]:
    return parse_motslettres_txt("mots8lettrespage1.txt")
