import pytest
from wordlefilegenerator.wordlefilegenerator import (
    ScraperError,
    extract_page_count_from_listesdemots_html,
    parse_html,
)

INVALID_PAGE_COUNT_INTEGER = """
<html>
    <body>
        <a class="pg" href="https://www.listesdemots.net/mots6lettrespage2.htm">2</a>
        <a class="pg" href="https://www.listesdemots.net/mots6lettrespage3.htm">3</a>
        <a class="pg" href="https://www.listesdemots.net/mots6lettrespage4.htm">4</a>
        ...
        <a class="pg" href="https://www.listesdemots.net/mots6lettrespage42.htm">invalid</a>
    </body>
</html>
"""

HTML_WITHOUT_PAGE_ANCHORS = """<html><body></body></html>"""


def test_e_p_c_f_l_h__success(mots8lettrespage1_html: str) -> None:
    assert (
        extract_page_count_from_listesdemots_html(parse_html(mots8lettrespage1_html))
        == 144
    )


def test_e_p_c_f_l_h__page_count_integer_cast_fails__raises_exception() -> None:
    with pytest.raises(ScraperError):
        extract_page_count_from_listesdemots_html(
            parse_html(INVALID_PAGE_COUNT_INTEGER)
        )


def test_e_p_c_f_l_h__when_no_page_anchors__returns_1(
    mots8lettrespage1_html: str,
) -> None:
    assert (
        extract_page_count_from_listesdemots_html(parse_html(HTML_WITHOUT_PAGE_ANCHORS))
        == 1
    )
