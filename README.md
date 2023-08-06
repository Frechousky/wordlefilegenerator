# wordlefilegenerator

CLI app to generate wordle files, ie. files containing fixed length words (eg. 6 characters length words).
Words are in lowercase and one word per line.
See [allmots4lettres.txt](tests/data/allmots4lettres.txt) for wordle file example.

## Install

- `make venv` to create virtualenv (optional)
- `make deps` to install dependencies

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
