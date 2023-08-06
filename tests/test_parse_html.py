import bs4
from wordlefilegenerator.wordlefilegenerator import parse_html


def test_parse_html__valid_return_type():
    assert type(parse_html("<html></html>")) == bs4.BeautifulSoup
