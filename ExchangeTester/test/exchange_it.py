import unittest
from ExchangeContract.generated_files.exchange_pb2 import *
from ExchangeTester.main.ExchangeFrontend import ExchangeFrontend

EXCHANGE_HOST = "localhost"
EXCHANGE_PORT = 8082


class ExchangeIT(unittest.TestCase):
    # TODO IMPLEMENT THIS
    frontend = ExchangeFrontend(EXCHANGE_HOST, EXCHANGE_PORT)


if __name__ == '__main__':
    unittest.main()
