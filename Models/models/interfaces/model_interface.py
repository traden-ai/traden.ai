from abc import ABC, abstractmethod


class ModelInterface(ABC):

    description = "default description for model"

    input_data = {}

    def get_description(self):
        return self.description

    def get_input_data(self):
        return self.input_data

    def set_input_data(self, input_data: set):
        self.input_data = input_data

    @abstractmethod
    def execute(self, daily_data: dict):
        """Executes actions for a certain day in the respective runnable
        ----------------------------------------------------------------------------------
        Daily_data  is of the form
        {Tradable_ticker_1: {"RSI" : 54.7352, ...}}
        ----------------------------------------------------------------------------------
        Output List is of the form
        [{"Ticker": ticker, "Action": Action, "Intensity": float}, ...], Buy_Percentage
        float between 0..1 representing intensity, the intensity should be non increasing,
        Buy_Percentage is a float between 0 and 1 representing the amount one wants to buy of a stock when compared
        to the ledger capital
        """
        pass

    def save_attributes(self) -> None:
        """Saves class attributes if needed for serialization purposes,
        for more information check jsonpickle restrictions"""
        pass

    def retrieve_attributes(self) -> None:
        """Retrieves class attributes if needed for deserialization purposes,
        this function should work as the inverse of save_attributes"""
        pass
