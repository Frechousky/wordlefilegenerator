# WORDLEFILEGENERATOR

CLI app to generate wordle files, ie. files containing fixed length words (eg. 6 characters length words).
Words are in lowercase and one word per line.
See [allmots4lettres.txt](tests/data/allmots4lettres.txt) for wordle file example.
Generates french words only and retrieves words from [1mot.net](https://1mot.net/).

## What is wordle ?

Wordle is a free online word game developed in 2021 by Josh Wardle.
This game is a direct adaptation of the American television game Lingo which asks you to guess a word
through several attempts, indicating for each of them the position of the well-placed and misplaced letters.
(source: Google)

## Require

- python ^3.11
- [poetry](https://python-poetry.org/)

## Install

- `make install-deps` to install dependencies

## Usage

```bash
Usage: wordlefilegenerator.py [OPTIONS] WORD_LENGTH

  Retrieve french words with specific length (character count) from internet
  and store them in a file, one word per line in lowercase.

Options:
  -o, --outputdir TEXT      Output directory to generate txt file
  -f, --outputfilefmt TEXT  Output filename format string (formats it with
                            WORD_LENGTH)
  -v, --verbose             print more output
  -s, --silent              print no ouput (ignore verbose)
  --help                    Show this message and exit.
```
