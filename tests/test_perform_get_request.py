from unittest.mock import Mock, patch
import pytest

import requests as rqsts

from wordlefilegenerator.wordlefilegenerator import ScraperError, perform_get_request


URL = "https://www.google.com"
HTML = "<html></html>"


@patch("wordlefilegenerator.wordlefilegenerator.rqsts.get")
def test_perform_get_request__success(mock_get: Mock) -> None:
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = HTML

    assert perform_get_request(URL) == HTML


@patch("wordlefilegenerator.wordlefilegenerator.rqsts.get")
def test_perform_get_request__request_failure__raises_exception(mock_get: Mock) -> None:
    mock_get.side_effect = rqsts.RequestException
    with pytest.raises(rqsts.RequestException):
        perform_get_request(URL)


@patch("wordlefilegenerator.wordlefilegenerator.rqsts.get")
@pytest.mark.parametrize("status_code", [range(300, 600)])
def test_perform_get_request__response_status_code_not_2XX__raises_exception(
    mock_get: Mock, status_code: int
) -> None:
    mock_get.return_value.status_code = status_code
    with pytest.raises(ScraperError):
        perform_get_request(URL)
