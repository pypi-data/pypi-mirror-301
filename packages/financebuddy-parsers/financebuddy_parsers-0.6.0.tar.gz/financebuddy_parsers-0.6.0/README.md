![](https://img.shields.io/badge/pypi-0.6.0-blue)
![](https://img.shields.io/badge/python-3.12-blue)
![](https://img.shields.io/badge/license-GPLv3.0-blue)

# financebuddy-parsers

Financial data parsers supported by [FinanceBuddy](https://github.com/cedricduriau/financebuddy).

## Installing

`financebuddy-parsers` can be installed using [pip](https://pypi.org/project/pip/).

```sh
pip install financebuddy-parsers
```

## What is FinanceBuddy?

Please read the [README](https://github.com/cedricduriau/financebuddy/blob/main/README.md).

## What are parsers?

A parser is a tool transforming financial data from a specific bank into a centralized format. Every parser is linked to a format and an extension.

- the `format` is driven by the bank the data is coming from
- the `extension` is driven by the file format the data is stored in

## Available parsers

| Bank                          | Country   | Format        | Extension  |
--------------------------------|-----------|---------------|------------|
| Argenta                       | 🇧🇪        | argenta-be    | xlsx       |
| BNP Parisbas Fortis           | 🇧🇪        | bnp-be        | csv        |
| ING                           | 🇧🇪        | ing-be        | csv        |
| Keytrade                      | 🌐        | keytrade      | csv        |
| Revolut                       | 🌐        | revolut       | csv        |

## FAQ

### What does the globe emoji mean as country for parsers?

Whenever a parser has the globe emoji 🌐 set as value for country, this means that there is only one format for all their supported countries/territories.

### Why is there a specific country mentioned for some parsers?

Some banks have a specific format per country. The format or even the extension could be different. To differenciate them, the country code is embedded in the format for clarity.

An example is between ING Belgium or ING Netherlands where both export a .CSV file but differ in file structure.

## Development

### Install
```sh
python -m venv .env
source .env/bin/activate
make install-dev
```
