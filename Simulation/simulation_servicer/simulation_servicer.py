from SimulationContract.generated_files import simulation_pb2_grpc, simulation_pb2


class SimulationServicer(simulation_pb2_grpc.SimulationServicer):

    def __init__(self, data_provider_frontend):
        self.data_provider_frontend = data_provider_frontend

    def ctrl_ping(self, request, context):
        return simulation_pb2.CtrlPingResponse(output=request.input)

    def list_model_instances(self, request, context):
        pass

    def delete_model_instances(self, request, context):
        pass

    def start_simulation(self, request, context):
        pass

    def simulation_graph(self, request, context):
        pass

    def simulation_logs(self, request, context):
        pass

    def close_simulation(self, request, context):
        pass
