from Exchange.endpoints.endpoint_interface import EndpointInterface
import Exchange.endpoints.kraken.utils as utils
import krakenex
from pykrakenapi import KrakenAPI
from datetime import date

class KrakenHandler(EndpointInterface):

    """notes:
    >maybe description is not required (depends on main exchange module impl)
    >should we introduce kraken libraries dependencies or implement request / retries
    >last_id is the id of last made info request to kraken
    """

    def __init__(self) -> None:
        name = "Kraken"
        description = "Exchange for cryptocurrencies"
        super().__init__(name, description)

        api = krakenex.API()
        self.k = KrakenAPI(api)
        self.last_id = {}

    def buy(self, tickers: dict):
        pass

    def sell(self, tickers: dict):
        pass

    def get_current_prince(self, ticker: str):

        """
        gets current price date from kraken,
        >find_latest_data should give the lates date in db
        >gets close price for all dates missing
        >returns {"2021-09-03": 24.24, "2021-09-04": 25.34} ... example values
        # integration untested
        # need to implement find latest data
        """

        # default for last is 1
        if (ticker not in self.last_id):
            self.last_id[ticker] = 1

        ohlc, last = self.k.get_ohlc_data(ticker, interval=1440, since=self.last_id[ticker])
        available_date = utils.find_latest_data(ticker)
        self.last_id = last

        res = {}

        # FIXME concerns about speed
        for id, close in zip(ohlc.index, ohlc["close"]):
            if (id == date.fromisoformat(available_date)):
                break

            res[id.date().isoformat()] = close

        return res
