from App.app.utils import *
from SimulationContract.generated_files import simulation_pb2


class Commands:

    def __init__(self, frontend):
        self.frontend = frontend

    def nothing():
        pass

    def ctrl_ping(self):
        req = simulation_pb2.CtrlPingRequest(input="hello")
        res = self.frontend.ctrl_ping(req)
        print("\n\tOutput: {}", res.output)

    def do_simulation(self):
        req = simulation_pb2.ListInstancesRequest()
        res = self.frontend.list_model_instances(req)

        balance, stocks, start_date, end_date, model_instances, no_exec = ask_simulation(res.instances)

        req = simulation_pb2.StartSimulationRequest(
            balance=balance,
            tickers=stocks,
            interval=simulation_pb2.TimeInterval(start_date=start_date, end_date=end_date),
            models=model_instances,
            number_executions=no_exec)

        res = self.frontend.start_simulation(req)
        status = res.status

        if (status == simulation_pb2.StartSimulationResponse.Status.OK):
            render_simulation(res.simulation_result)
            if (ask_graph()):
                req = simulation_pb2.SimulationGraphRequest(simulation_id=res.simulation_result.simulation_id)
                stream, status = self.frontend.simulation_graph(req)
                #FIXME account for status
                render_graph(stream)

            #TODO prompt logs

        elif (status == simulation_pb2.StartSimulationResponse.Status.TICKERS_NOT_AVAILABLE):
            tickers = res.tickers
            print("\n\tERROR: The following tickers are not available")
            [print(f"\t\t{t}") for t in tickers.not_available_tickers]

        elif (status == simulation_pb2.StartSimulationResponse.Status.INTERVAL_NOT_AVAILABLE):
            interval = res.interval
            print(res)
            print(f"\n\tERROR: Requested stocks are only available from {interval.start_date} to {interval.end_date}")

        elif (status == simulation_pb2.StartSimulationResponse.Status.MODEL_INSTANCES_NOT_AVAILABLE):
            print("\n\tERROR: Requested instance isn't available")

        else:
            print("\n\tERROR: Unexpected error ocurred")

    def delete_model_instances(self):

        req = simulation_pb2.ListInstancesRequest()
        res = self.frontend.list_model_instances(req)
        instances = ask_model_instances(res.instances)
        
        req = simulation_pb2.DeleteInstancesRequest(instances=instances)
        res = self.frontend.delete_model_instances(req)
        # FIXME check for errors? implies changing proto

    def close_simulation(self):  

        # TODO multiple simulations
        id = ask_simulation_id()
        req = simulation_pb2.CloseSimulationRequest(simulation_id=id)
        res = self.frontend.close_simulation(req)

        if (res.status == simulation_pb2.CloseSimulationResponse.Status.OK):
            print("\n\tSimulation closed successfully\n")
        else:
            # FIXME specify id not found
            print("\n\tERROR: Unexpected error ocurred\n")

    def help_instructions(self):
        print("\n+\n|\t% Application Description\n|")
        print("|\t\tThis application presents a tool to simulate mathematical")
        print("|\t\ttrading models, using real data from previous years\n|")
        print("|\t% Commands\n|")
        print("|\t\th\tOpen the help instructions.\n|")
        print("|\t\ts\tCreate a stock trading model simulation.\n|")
        print("|\t\txs\tClose simulation.\n|")
        print("|\t\txi\tClear model instance.\n|")
        print("|\t\tq\tQuit the application.\n+\n")
