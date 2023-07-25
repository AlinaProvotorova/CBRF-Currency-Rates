import argparse


def configure_currency_parser():
    parser = argparse.ArgumentParser(
        description='Get currency rates from the Central Bank of Russia.'
    )
    parser.add_argument(
        '-c', '--code',
        type=str, required=True,
        help='Currency from the Central Bank of Russia'
    )
    parser.add_argument(
        '-d', '--date',
        type=str, required=True,
        help='Date in the format YYYY-MM-DD'
    )
    return parser
