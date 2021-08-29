from App.exchange.utils import *
from ExchangeContract.generated_files import exchange_pb2


class ExchangeCommands:

    def __init__(self, frontend):
        self.frontend = frontend

    def parser(self, command):

        switcher = {
            "": self.nothing,
            "h": self.help_instructions,
            "s": self.start_model,
            "xs": self.stop_model,
            "c": self.change_capital,
            "t": self.add_tickers,
            "xt": self.remove_tickers,
            "l": self.ledger_info,
            "m": self.model_info,
            "p": self.ctrl_ping,
            "q": None
        }

        return switcher.get(command, lambda: print("\n\tERROR: Invalid command.\n\tPlease insert 'h' for help.\n"))

    def nothing():
        pass

    def ctrl_ping(self):
        req = exchange_pb2.CtrlPingRequest(input="hello")
        res = self.frontend.ctrl_ping(req)
        print("\n\tOutput: {}", res.output)
        

    def start_model(self):
        
        # FIXME get instances
        instance = ask_model(None)
        tickers = ask_stocks()
        capital = ask_balance()
        
        request = exchange_pb2.StartModelRequest(
            model=instance,
            tickers=tickers,
            capital=capital 
        )

        response = self.frontend.start_model(request)
        status = response.status
        
        if (status == exchange_pb2.ExchangeResponseStatus.OK):
            print("Model start sucessful")
        elif (status == exchange_pb2.ExchangeResponseStatus.MODEL_NOT_FOUND):
            print("Model not found")
        elif (status == exchange_pb2.ExchangeResponseStatus.MONEY_NOT_FOUND):
            print("Money not found")
        elif (status == exchange_pb2.ExchangeResponseStatus.TICKERS_NOT_FOUND):
            print("Tickers not found")
        elif (status == exchange_pb2.ExchangeResponseStatus.NOK):
            print("Something went wrong in API call")


    def stop_model(self):

        # FIXME get instances
        instance = ask_model(None)
        request = exchange_pb2.StopModelRequest(
            model=instance
        )
        
        response = self.frontend.stop_model(request)
        status = response.status

        if (status == exchange_pb2.ExchangeResponseStatus.OK):
            print("Model was stopped successfully")
        elif (status == exchange_pb2.ExchangeResponseStatus.MODEL_NOT_FOUND):
            print("Model not found")
        elif (status == exchange_pb2.ExchangeResponseStatus.NOK):
            print("Something went wrong in API call")

    def change_capital(self):

        # FIXME get instances
        instance = ask_model(None)
        capital = ask_balance()
        
        if (capital > 0):
            self.add_capital(instance, capital)
        elif (capital < 0):
            self.remove_capital(instance, capital)

    def add_capital(self, instance, capital):

        request = exchange_pb2.AddCapitalToModelRequest(
            model=instance,
            capital=capital
        )

        response = self.frontend.add_capital_to_model(request)
        status = response.status

        if (status == exchange_pb2.ExchangeResponseStatus.OK):
            print("Capital added successfully")
        elif (status == exchange_pb2.ExchangeResponseStatus.MODEL_NOT_FOUND):
            print("Model not found")
        elif (status == exchange_pb2.ExchangeResponseStatus.MONEY_NOT_FOUND):
            print("Money not found")
        elif (status == exchange_pb2.ExchangeResponseStatus.NOK):
            print("Something went wrong in API call")
        

    def remove_capital(self, instance, capital):

        request = exchange_pb2.RemoveCapitalFromModelRequest(
            model=instance,
            capital=capital
        )

        response = self.frontend.remove_capital_from_model(request)
        status = response.status

        if (status == exchange_pb2.ExchangeResponseStatus.OK):
            print("Capital removed successfully")
        elif (status == exchange_pb2.ExchangeResponseStatus.MODEL_NOT_FOUND):
            print("Model not found")
        elif (status == exchange_pb2.ExchangeResponseStatus.MONEY_NOT_FOUND):
            print("Money not found")
        elif (status == exchange_pb2.ExchangeResponseStatus.NOK):
            print("Something went wrong in API call")
    
    def add_tickers(self):

        instance = ask_model(None)
        tickers = ask_stocks()

        request = exchange_pb2.AddTickersToModelRequest(
            model=instance,
            tickers=tickers
        )

        response = self.frontend.add_tickers_to_model(request)
        status = response.status

        if (status == exchange_pb2.ExchangeResponseStatus.OK):
            print("Tickers added successfully")
        elif (status == exchange_pb2.ExchangeResponseStatus.MODEL_NOT_FOUND):
            print("Model not found")
        elif (status == exchange_pb2.ExchangeResponseStatus.TICKERS_NOT_FOUND):
            print("Tickers not found")
        elif (status == exchange_pb2.ExchangeResponseStatus.NOK):
            print("Something went wrong in API call")
    

    def remove_tickers(self):

        instance = ask_model(None)
        tickers = ask_stocks()

        request = exchange_pb2.RemoveTickersFromModelRequest(
            model=instance,
            tickers=tickers
        )

        response = self.frontend.remove_tickers_from_model(request)
        status = response.status

        if (status == exchange_pb2.ExchangeResponseStatus.OK):
            print("Tickers removed successfully")
        elif (status == exchange_pb2.ExchangeResponseStatus.MODEL_NOT_FOUND):
            print("Model not found")
        elif (status == exchange_pb2.ExchangeResponseStatus.TICKERS_NOT_FOUND):
            print("Tickers not found")
        elif (status == exchange_pb2.ExchangeResponseStatus.NOK):
            print("Something went wrong in API call")
    
    def ledger_info(self):
        request = exchange_pb2.LedgerInfoRequest()
        response = self.frontend.ledger_info(request)

        #FIXME display ledger

    def model_info(self):

        instance = ask_model(None)
        request = exchange_pb2.ModelInfoRequest(
            model=instance
        )       
        response = self.frontend.model_info(request)

        #FIXME display model/ledger

    def help_instructions():
        print("\n+\n|\t% Application Description\n|")
        print("|\t\tThis application presents a tool to simulate mathematical")
        print("|\t\ttrading models, using real data from previous years\n|")
        print("|\t% Commands\n|")
        print("|\t\th\tOpen the help instructions.\n|")
        print("|\t\ts\tStart trading with a model.\n|")
        print("|\t\txs\tStop trading with a model.\n|")
        print("|\t\tc\tChange capital allocated to a model.\n|")
        print("|\t\tt\tAdd tickers to a model.\n|")
        print("|\t\tx\tRemove tickers to a model.\n|")
        print("|\t\tl\tDisplay ledger data\n|")
        print("|\t\tm\tDisplay model data\n|")
        print("|\t\tq\tQuit mode.\n+\n")
