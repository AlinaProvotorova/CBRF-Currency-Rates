import unittest
from unittest.mock import patch

from src import currency_rates


class TestCurrencyRates(unittest.TestCase):

    @patch("currency_rates.requests.get")
    def test_get_currency_rates_valid_response(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.content = r"""<?xml version="1.0" encoding="UTF-8"?>
            <ValCurs Date="08.10.2022" name="Foreign Currency Market">
                <Valute ID="R01010">
                    <NumCode>036</NumCode>
                    <CharCode>USD</CharCode>
                    <Nominal>1</Nominal>
                    <Name>Доллар США</Name>
                    <Value>39,2290</Value>
                </Valute>
            </ValCurs>
        """

        result = currency_rates.get_currency_rates("USD", "2022-10-08")
        self.assertEqual(result, "USD (Доллар США): 39,2290")

    @patch("currency_rates.requests.get")
    def test_get_currency_rates_invalid_response(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        with self.assertRaises(ConnectionError):
            currency_rates.get_currency_rates("USD", "2022-10-08")

    @patch("currency_rates.requests.get")
    def test_get_currency_rates_currency_not_found(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.content = r"""<?xml version="1.0" encoding="UTF-8"?>
            <ValCurs Date="08.10.2022" name="Foreign Currency Market">
                <Valute ID="R01010">
                    <NumCode>036</NumCode>
                    <CharCode>AUD</CharCode>
                    <Nominal>1</Nominal>
                    <Name>Австралийский доллар</Name>
                    <Value>39,2290</Value>
                </Valute>
            </ValCurs>
        """

        with self.assertRaises(ValueError):
            currency_rates.get_currency_rates("USD", "2022-10-08")


if __name__ == "__main__":
    unittest.main()
