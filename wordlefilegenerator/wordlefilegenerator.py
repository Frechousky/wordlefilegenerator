#!/usr/bin/env python3.11
"""
CLI app to retrieve french words with specific length (character count) from internet
and store them in a file, one word per line in lowercase.
FMI about usage run ./wordlefilegenerator.py -h
"""
import os
import sys

import bs4
import click
import requests as rqsts
from loguru import logger


class WordExtractionError(Exception):
    """Errors when extracting words from HTML"""

    pass


class ScraperError(Exception):
    """Errors when scrapping"""

    pass


def perform_get_request(url: str) -> str:
    """
    Perform a GET request to specified URL and returns decoded response content

    Args:
        url (str): URL to request

    Raises:
        rqsts.RequestException: if GET request fail
        ScraperError: if response status code is not 2XX

    Returns:
        decoded response content
    """
    r = rqsts.get(url)
    if r.status_code not in range(200, 300):
        raise ScraperError(f"Request to {r.url} returned HTTP code {r.status_code}")
    return r.text


def parse_html(html: str) -> bs4.BeautifulSoup:
    """
    Parse HTML with BeautifulSoup.

    Args:
        html (str): HTML string to parse

    Returns:
        Parsed HTML
    """
    return bs4.BeautifulSoup(html, "html.parser")


def extract_words_from_listesdemots_html(parsed_html: bs4.BeautifulSoup) -> list[str]:
    """
    Parse HTML from [listesdemots](https://www.listesdemots.net/) to extract words
    list.

    Words are contained inside tag <span class="mt">WORD1 WORD2 ... WORDN</span>
    in uppercase and seperated by space.
    Retrieve this <span> and extract lowercase list of words from it.

    Args:
        parsed_html: bs4.BeautifulSoup initialized with HTML from [listesdemots](https://www.listesdemots.net/)

    Returns:
        List of words in lowercase.

    Raises:
        WordExtractionError: if <span> tag containing word is not present in HTML
    """
    word_span = parsed_html.find("span", {"class": "mt"})
    if word_span is None:
        raise WordExtractionError(
            f'Error finding <span class="mt"> containing words from HTML:\n \
            {parsed_html.prettify()}'
        )
    logger.debug('Found <span class="mt"> tag')

    # words are in uppercase and separated by spaces
    words = word_span.string.lower().replace("\n", "").split(" ")
    words = [w for w in words if w != ""]
    logger.info(f"Parsed {len(words)} words")
    return words


def extract_page_count_from_listesdemots_html(parsed_html: bs4.BeautifulSoup) -> int:
    """
    Retrieve page count.

    Words list may be paginated, look for pagination anchors to retrieve page count
    When there is no pagination anchors there is one page.
    Pagination anchors are contained in <a> tag:
        <a class="pg" href="link2">2</a>
        <a class="pg" href="link3">3</a>
        <a class="pg" href="link4">4</a>
        ... (remark: there is litteraly 3 dots)
        <a class="pg" href="linkn">n</a>
    Retrieve "n" which is page count.
    There should be 4 anchors.
    If there is no pagination anchors, returns 1.

    Returns:
        Page count

    Raises:
        ScraperError: if page count integer cast fail
    """
    pagination_anchors = parsed_html.find_all("a", {"class": "pg"})
    if pagination_anchors is None or len(pagination_anchors) == 0:
        logger.debug("No page anchors found in HTML")
        logger.debug("There is only one page")
        return 1
    logger.debug(
        "Found {} pagination anchors, retrieve page count", len(pagination_anchors)
    )
    last_anchor = pagination_anchors.pop()
    try:
        page_count = int(last_anchor.string)
        logger.debug(f"Page count: {page_count}")
        return page_count
    except ValueError:
        raise ScraperError(
            f"Error retrieving page count, could not cast {last_anchor.string} to \
                an integer"
        )


FIRST_PAGE_URL_FMT = "https://www.listesdemots.net/mots{}lettres.htm"
NTH_PAGE_URL_FMT = "https://www.listesdemots.net/mots{}lettrespage{}.htm"


def scrap_listesdemots(word_length: int) -> list[str]:
    """
    Retrieve french words with specific character length from [listesdemots](https://www.listesdemots.net/).


    Words list is paginated on several HTML-pages, therefore we first have to
    retrieve number of page from HTML. For each page, we retrieve HTML content
    then extract words from it.

    Args:
        word_length: character length of words to retrieve

    Returns:
        List of lowercase words with {word_length} characters

    Raises:
        rqsts.RequestException: if GET request to listesdemots fail (timeout, ...)
        ScraperError: if GET request to listesdemots returns status code != 2XX
        ScraperError: if page count integer cast fail
        WordExtractionError: if extraction fail
                             (see extract_words_from_listesdemots_html)
    """
    parsed_html = parse_html(
        perform_get_request(FIRST_PAGE_URL_FMT.format(word_length))
    )

    page_count = extract_page_count_from_listesdemots_html(parsed_html)

    logger.debug(f"Start extracting word with {word_length} characters")
    logger.info("Parse page 1/{}", page_count)
    words = extract_words_from_listesdemots_html(parsed_html)
    for page in range(2, page_count + 1):
        logger.info("Parse page {}/{}", page, page_count)
        parsed_html = parse_html(
            perform_get_request(NTH_PAGE_URL_FMT.format(word_length, page))
        )
        words = words + extract_words_from_listesdemots_html(parsed_html)
    logger.info(f"Word parsing is successful, {len(words)} words parsed")
    return words


def init_loguru(verbose: bool, silent: bool) -> None:
    """
    Init loguru logger.

    Remove basic logger.
    Add new logger to stderr with DEBUG (if verbose) or INFO level.
    Add handler to intercept standard logging messages with loguru.

    Args:
        verbose: set logs level to DEBUG if verbose, else INFO
        silent: does not log anything (verbose is ignored)

    Returns:
        None
    """
    # cannot update level of default logger
    # we have to remove it then add a new one
    # see https://github.com/Delgan/loguru/issues/138
    logger.remove()

    if silent:
        return

    logger.add(
        sys.stderr,
        level="DEBUG" if verbose else "INFO",
        format="{message}",
    )

    # intercept standard logging messages with loguru
    # useful to get logs from libraries
    # see https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    import logging

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists.
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message.
            frame, depth = sys._getframe(6), 6
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


@click.command()
@click.argument("word_length", type=int)
@click.option(
    "--outputdir", "-o", default=".", help="Output directory to generate txt file"
)
@click.option(
    "--outputfilefmt",
    "-f",
    default="words_{}_fr.txt",
    help="Output filename format string (formats it with WORD_LENGTH)",
)
@click.option("--verbose", "-v", is_flag=True, help="print more output")
@click.option("--silent", "-s", is_flag=True, help="print no ouput (ignore verbose)")
def wordlefilegenerator(
    word_length: int, outputdir: str, outputfilefmt: str, verbose: bool, silent: bool
):
    """
    Retrieve french words with specific length (character count) from internet and
    store them in a file, one word per line in lowercase.
    """
    init_loguru(verbose, silent)
    try:
        words = scrap_listesdemots(word_length)
    except (ScraperError, WordExtractionError, rqsts.RequestException) as e:
        logger.critical(f"Error scraping: {e}")
        logger.critical("Abort wordlefilegenerator")
        sys.exit(-1)
    fname = outputfilefmt.format(word_length)
    outputfile = os.path.join(outputdir, fname)
    try:
        with open(outputfile, "w") as f:
            f.write("\n".join(words))
            f.write("\n")
        logger.info("File generation is successful")
    except OSError as e:
        logger.critical(
            f'Error writing file "{outputfile}" to filesystem: {e.strerror}'
        )
        logger.critical("Abort wordlefilegenerator")
        sys.exit(-1)


if __name__ == "__main__":
    wordlefilegenerator()
