import xml.etree.ElementTree as ET
from datetime import datetime

import requests

from configs import configure_currency_parser
from constants import (
    CODE_VALUTE_XML, CRB_URL, DATE_FORMAT_INPUT, DATE_FORMAT_OUTPUT,
    NAME_VALUTE_XML, TAG_ROOT, VALUE_VALUTE_XML
)


def format_date(date_str):
    date_obj = datetime.strptime(date_str, DATE_FORMAT_INPUT)
    return date_obj.strftime(DATE_FORMAT_OUTPUT)


ERROR_CONNECT = 'Failed to retrieve data from the Central Bank of Russia.' \
                'Error code: {}'

ERROR_NOT_FOUND = 'Currency with code {} not found for the specified date {}.'


def get_currency_rates(code, date):
    response = requests.get(CRB_URL.format(format_date(date)))
    if response.status_code != 200:
        raise ConnectionError(ERROR_CONNECT.format(response.status_code))

    root = ET.fromstring(response.content)
    for currency in root.findall(TAG_ROOT):
        if currency.find(CODE_VALUTE_XML).text.lower() == code.lower():
            name = currency.find(NAME_VALUTE_XML).text
            value = currency.find(VALUE_VALUTE_XML).text
            return f"{code} ({name}): {value}"

    raise ValueError(ERROR_NOT_FOUND.format(code, date))


def main():
    arg_parser = configure_currency_parser()
    args = arg_parser.parse_args()

    try:
        print(get_currency_rates(args.code, args.date))
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
