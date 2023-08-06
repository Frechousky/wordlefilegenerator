import pytest

from wordlefilegenerator.wordlefilegenerator import (
    WordExtractionError,
    extract_words_from_listesdemots_html,
    parse_html,
)


def test_e_w_f_m_h__success(
    mots6lettrespage1_html: str,
    mots6lettrespage1: list[str],
    mots8lettrespage1_html: str,
    mots8lettrespage1: list[str],
):
    assert (
        extract_words_from_listesdemots_html(parse_html(mots6lettrespage1_html))
        == mots6lettrespage1
    )
    assert (
        extract_words_from_listesdemots_html(parse_html(mots8lettrespage1_html))
        == mots8lettrespage1
    )


def test_e_w_f_m_h__if_html_does_not_containt_words__raises_exception():
    with pytest.raises(WordExtractionError):
        extract_words_from_listesdemots_html(parse_html("<html>It's a me</html>"))
