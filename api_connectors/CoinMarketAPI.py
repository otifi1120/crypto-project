from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class CoinMarketCapAPI:
    _instance = None

    def __new__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__new__(self)
        return self._instance

    def __init__(self):
        self._api_key = self._get_api_key()
        self.convert = 'BTC,USD,ETH,BNB'

    def _get_api_key(self):
        with open('credentials', 'r') as file:
            for line in file:
                if line.startswith('coinMarketCap='):
                    return line.strip().split('=')[1]

    def _make_request(self, url, parameters, headers):
        try:
            session = Session()
            request = Request('GET', url, headers=headers, params=parameters)
            prepared_request = request.prepare()
            response = session.send(prepared_request)

            data = json.loads(response.text)['data']

            return data

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

    def get_crypto_data(self):
        url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': '1',
            'limit': '5000',
            'convert': self.convert
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self._api_key,
        }
        return self._make_request(url, parameters, headers)

