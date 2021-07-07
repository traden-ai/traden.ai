from Simulation.utils.utils import *
from Models.models.model_interface import Action, TradingData
from Simulation.simulation.simulation_assembler import SimulationAssembler
from DataProviderContract.generated_files import data_provider_pb2
from SimulationContract.generated_files import simulation_pb2_grpc, simulation_pb2
from Models.model_database_handler.model_database_handler import list_instances, delete_instance, get_instance


class SimulationServicer(simulation_pb2_grpc.SimulationServicer):

    def __init__(self, data_provider_frontend, logger):
        self.open_assemblers = {}
        self.data_provider_frontend = data_provider_frontend
        self.logger = logger

    def ctrl_ping(self, request, context):
        self.logger.info(f"Received 'ctrl_ping'")
        return simulation_pb2.CtrlPingResponse(output=request.input)

    def list_model_instances(self, request, context):
        self.logger.info("Received 'list_model_instances'")
        return simulation_pb2.ListInstancesResponse(instances=list_instances())

    def delete_model_instances(self, request, context):
        self.logger.info(f"Received 'delete_model_instances'")
        instances = request.instances
        for instance in instances:
            delete_instance(instance)
        return simulation_pb2.DeleteInstancesResponse()

    def start_simulation(self, request, context):
        self.logger.info("Received 'start_simulation'")
        # get model instances
        model_instances = []
        for model in request.models:
            instance = get_instance(model)
            if instance:
                model_instances.append(instance)
            else:
                return simulation_pb2.StartSimulationResponse(
                    status=simulation_pb2.StartSimulationResponse.Status.MODEL_INSTANCES_NOT_AVAILABLE
                )

        # get data requested by models
        data_request = {TradingData.dailyAdjusted}  # price is always needed
        for instance in model_instances:
            data_request = data_request.union(instance.get_input_data())

        # get data from data provider
        response, status = self.data_provider_frontend.get_past_data(data_provider_pb2.PastDataRequest(
                tickers=request.tickers,
                indicators=map(lambda trading_data: trading_data.name, data_request),
                interval=data_provider_pb2.TimeInterval(
                    start_date=request.interval.start_date,
                    end_date=request.interval.end_date
                )
            ))

        if status == data_provider_pb2.PastDataResponse.Status.NOK:
            return simulation_pb2.StartSimulationResponse(
                status=simulation_pb2.StartSimulationResponse.Status.NOK
            )
        if status == data_provider_pb2.PastDataResponse.Status.TICKERS_NOT_AVAILABLE:
            return simulation_pb2.StartSimulationResponse(
                status=simulation_pb2.StartSimulationResponse.Status.TICKERS_NOT_AVAILABLE,
                tickers=simulation_pb2.TickerList(
                    available_tickers=response["tickers"].available_tickers,
                    not_available_tickers=response["tickers"].not_available_tickers
                )
            )
        if status == data_provider_pb2.PastDataResponse.Status.INTERVAL_NOT_AVAILABLE:
            return simulation_pb2.StartSimulationResponse(
                status=simulation_pb2.StartSimulationResponse.Status.INTERVAL_NOT_AVAILABLE,
                interval=simulation_pb2.TimeInterval(
                    start_date=response["interval"].start_date,
                    end_date=response["interval"].end_date
                )
            )

        if status == data_provider_pb2.PastDataResponse.Status.OK:

            # process data
            dates, data, prices = data_load(response["data"])

            # create and execute simulation assembler
            try:
                assembler = SimulationAssembler(request.balance, request.tickers, model_instances, dates, data, prices,
                                                request.transaction_fee, request.number_executions)
                assembler.execute()
            except Exception:
                self.logger.exception("Caught an exception while execution a simulation")
                return simulation_pb2.StartSimulationResponse(status=simulation_pb2.StartSimulationResponse.Status.NOK)

            # save opened simulation assembler
            assembler_id = 0
            while assembler_id in self.open_assemblers:
                assembler_id += 1
            self.open_assemblers[assembler_id] = assembler

            # send simulation results
            return simulation_pb2.StartSimulationResponse(
                status=simulation_pb2.StartSimulationResponse.Status.OK,
                simulation_result=simulation_pb2.SimulationResult(
                    simulation_id=assembler_id,
                    model_results=[simulation_pb2.ModelResults(
                        model=simulation.model.__class__.__name__,
                        nominal_profit=simulation.avg_results["profit"],
                        percentage_profit=simulation.avg_results["profit_percentage"],
                        yearly_percentage_profit=simulation.avg_results["profit_percentage_year"],
                        operating_time_percentage=simulation.avg_results["operating_time_percentage"]
                    ) for simulation in assembler.get_ordered_simulations()],
                    ticker_results=[simulation_pb2.TickerResults(
                        ticker=ticker,
                        percentage_profit=assembler.simulations[0].results[0]["stocks_performance"][ticker]  # FIXME
                    ) for ticker in assembler.tradable_tickers]
                )
            )

        else:
            return simulation_pb2.StartSimulationResponse(
                status=simulation_pb2.StartSimulationResponse.Status.NOK
            )

    def simulation_graph(self, request, context):
        self.logger.info("Received 'simulation_graph'")
        assembler_id = request.simulation_id
        if assembler_id in self.open_assemblers:
            assembler = self.open_assemblers[assembler_id]
            for no_sim in range(len(assembler.simulations)):
                model_name = assembler.simulations[no_sim].model.__class__.__name__
                graph = assembler.get_graph(no_sim)
                yield simulation_pb2.SimulationGraphResponse(
                    model=model_name,
                    data_points=[simulation_pb2.DataPoint(
                        time=data_point[0],
                        capital=data_point[1]
                    ) for data_point in graph],
                    status=simulation_pb2.SimulationGraphResponse.Status.OK
                )
        else:
            yield simulation_pb2.SimulationGraphResponse(
                status=simulation_pb2.SimulationGraphResponse.Status.SIMULATION_NOT_FOUND
            )

    def simulation_logs(self, request, context):
        self.logger.info("Received 'simulation_logs'")
        assembler_id = request.simulation_id
        if assembler_id in self.open_assemblers:
            assembler = self.open_assemblers[assembler_id]
            for no_sim in range(len(assembler.simulations)):
                for no_ex in range(1, assembler.no_executions + 1):
                    model = assembler.simulations[no_sim].model.__class__.__name__
                    logs = assembler.get_logs(no_sim, no_ex)
                    yield simulation_pb2.SimulationLogsResponse(
                        model=model,
                        number_execution=no_ex,
                        logs=[simulation_pb2.Log(
                            action=simulation_pb2.Log.Action.BUY if log["action"] == Action.BUY
                            else simulation_pb2.Log.Action.SELL,
                            amount=log["amount"],
                            ticker=log["ticker"],
                            price_per_share=log["price"],
                            date=log["date"]
                        ) for log in logs],
                        status=simulation_pb2.SimulationLogsResponse.Status.OK
                    )
        else:
            yield simulation_pb2.SimulationLogsResponse(
                status=simulation_pb2.SimulationLogsResponse.Status.SIMULATION_NOT_FOUND
            )

    def close_simulation(self, request, context):
        self.logger.info("Received 'close_simulation'")
        assembler_id = request.simulation_id
        if assembler_id in self.open_assemblers:
            self.open_assemblers.pop(assembler_id)
            return simulation_pb2.CloseSimulationResponse(
                status=simulation_pb2.CloseSimulationResponse.Status.OK
            )
        else:
            return simulation_pb2.CloseSimulationResponse(
                status=simulation_pb2.CloseSimulationResponse.Status.SIMULATION_NOT_FOUND
            )
