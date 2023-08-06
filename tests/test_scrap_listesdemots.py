from unittest.mock import Mock, patch
import pytest

import requests as rqsts

from wordlefilegenerator.wordlefilegenerator import (
    ScraperError,
    WordExtractionError,
    scrap_listesdemots,
)


@patch("wordlefilegenerator.wordlefilegenerator.perform_get_request")
def test_scrap__success(
    mock_pgr: Mock,
    mots4lettrespage1_html: str,
    mots4lettrespage2_html: str,
    mots4lettrespage3_html: str,
    mots4lettrespage4_html: str,
    mots4lettrespage5_html: str,
    allmots4lettres: list[str],
):
    mock_pgr.side_effect = [
        mots4lettrespage1_html,
        mots4lettrespage2_html,
        mots4lettrespage3_html,
        mots4lettrespage4_html,
        mots4lettrespage5_html,
    ]

    assert scrap_listesdemots(4) == allmots4lettres


@patch("wordlefilegenerator.wordlefilegenerator.perform_get_request")
def test_scrap__request_failure__raises_exception(mock_pgr: Mock):
    mock_pgr.side_effect = rqsts.RequestException

    with pytest.raises(rqsts.RequestException):
        scrap_listesdemots(6)


@patch("wordlefilegenerator.wordlefilegenerator.perform_get_request")
def test_scrap__response_status_code_not_2XX__raises_exception(mock_pgr: Mock):
    mock_pgr.side_effect = ScraperError

    with pytest.raises(ScraperError):
        scrap_listesdemots(6)


@patch("wordlefilegenerator.wordlefilegenerator.extract_page_count_from_listesdemots_html")
def test_scrap__page_count_integer_cast_fails__raises_exception(mock_epcflh: Mock):
    mock_epcflh.side_effect = ScraperError

    with pytest.raises(ScraperError):
        scrap_listesdemots(6)


@patch("wordlefilegenerator.wordlefilegenerator.extract_words_from_listesdemots_html")
def test_scrap__if_word_extraction_fails__raises_exception(mock_ewflh: Mock):
    mock_ewflh.side_effect = WordExtractionError

    with pytest.raises(WordExtractionError):
        scrap_listesdemots(6)
