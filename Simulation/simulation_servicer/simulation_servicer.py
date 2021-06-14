from Simulation.simulation.simulation_assembler import SimulationAssembler
from DataProviderContract.generated_files import data_provider_pb2
from SimulationContract.generated_files import simulation_pb2_grpc, simulation_pb2
from Models.model_database_handler.model_database_handler import list_instances, delete_instance, get_instance

MAX_SIMULATIONS = 1000


class SimulationServicer(simulation_pb2_grpc.SimulationServicer):

    def __init__(self, data_provider_frontend):
        self.open_assemblers = {}
        self.data_provider_frontend = data_provider_frontend

    def ctrl_ping(self, request, context):
        return simulation_pb2.CtrlPingResponse(output=request.input)

    def list_model_instances(self, request, context):
        return simulation_pb2.ListInstancesResponse(instances=list_instances())

    def delete_model_instances(self, request, context):
        instances = request.instances
        for instance in instances:
            delete_instance(instance)
        return simulation_pb2.DeleteInstancesResponse()

    def start_simulation(self, request, context):

        # get data from data provider
        response = self.data_provider_frontend.get_past_data(
            data_provider_pb2.PastDataRequest(
                tickers=request.tickers,
                # indicators= # TODO
                interval=data_provider_pb2.TimeInterval(initial_date=request.start_date, end_date=request.end_date)
            )
        )
        if response.status == data_provider_pb2.PastDataResponse.Status.NOK:
            return simulation_pb2.StartSimulationResponse(
                status=simulation_pb2.StartSimulationResponse.Status.NOK
            )
        if response.status == data_provider_pb2.PastDataResponse.Status.TICKERS_NOT_AVAILABLE:
            return simulation_pb2.StartSimulationResponse(
                status=simulation_pb2.StartSimulationResponse.Status.TICKERS_NOT_AVAILABLE
            )
        if response.status == data_provider_pb2.PastDataResponse.Status.DATE_NOT_AVAILABLE:
            return simulation_pb2.StartSimulationResponse(
                status=simulation_pb2.StartSimulationResponse.Status.INTERVAL_NOT_AVAILABLE,
                interval=simulation_pb2.TimeInterval(
                    start_date=response.interval.initial_date, end_date=response.interval.end_date
                )
            )

        # parse data from data_provider
        # data =  # TODO

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

        # create and execute simulation assembler
        try:
            assembler = SimulationAssembler(
                # request.balance, request.tickers, model_instances, data, request.no_executions
            )
            assembler.execute()
        except Exception as e:
            print("Caught an exception during a simulation: " + str(e))
            return simulation_pb2.StartSimulationResponse(status=simulation_pb2.StartSimulationResponse.Status.NOK)

        # save opened simulation assembler
        assembler_id = 0
        while assembler_id in self.open_assemblers:
            assembler_id += 1
            if assembler_id >= MAX_SIMULATIONS:
                return simulation_pb2.StartSimulationResponse(status=simulation_pb2.StartSimulationResponse.Status.NOK)
        self.open_assemblers[assembler_id] = assembler

        # send simulation results
        return simulation_pb2.StartSimulationResponse(
            # TODO
        )

    def simulation_graph(self, request, context):
        assembler = self.open_assemblers[request.simulation_id]
        for no_sim in range(len(assembler.simulations)):
            yield simulation_pb2.SimulationGraphResponse(
                # TODO
                graphs=assembler.get_graph(no_sim)
            )

    def simulation_logs(self, request, context):
        assembler = self.open_assemblers[request.simulation_id]
        for no_sim in range(len(assembler.simulations)):
            for no_ex in range(1, assembler.no_executions + 1):
                yield simulation_pb2.SimulationLogsResponse(
                    # TODO
                    logs=assembler.get_logs(no_sim, no_ex)
                )

    def close_simulation(self, request, context):
        assembler_id = request.simulation_id
        if assembler_id in self.open_assemblers:
            self.open_assemblers.pop(assembler_id)
            return simulation_pb2.CloseSimulationResponse(status=simulation_pb2.CloseSimulationResponse.Status.OK)
        else:
            return simulation_pb2.CloseSimulationResponse(status=simulation_pb2.CloseSimulationResponse.Status.NOK)
