import unittest
from app import app, currency_symbols

class CurrencyConverterTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_currency_symbol_lookup(self):
        self.assertEqual(currency_symbols['USD'], '$')
        self.assertEqual(currency_symbols['EUR'], '€')

    def test_convert_route_invalid_currency_symbol(self):
        response = self.app.post('/convert', data={
            'amount': '10',
            'from_currency': 'XYZ',
            'to_currency': 'EUR'
        })
        self.assertIn("Currency symbol doesn", response.data.decode())

    def test_convert_route_with_exception_handling(self):
        response = self.app.post('/convert', data={
            'amount': 'not_a_number',
            'from_currency': 'USD',
            'to_currency': 'EUR'
        })
        self.assertIn("could not convert string to float", response.data.decode())

    def test_convert_route(self):
        response = self.app.post('/convert', data={
            'amount': '10',
            'from_currency': 'USD',
            'to_currency': 'USD'
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
