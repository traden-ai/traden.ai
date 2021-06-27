import grpc

from SimulationContract.generated_files import simulation_pb2_grpc


class SimulationFrontend:
    def __init__(self, simulation_host, simulation_port):
        self.simulation_host = simulation_host
        self.simulation_port = simulation_port
        self.channel = grpc.insecure_channel(
            f"{simulation_host}:{simulation_port}")
        self.stub = simulation_pb2_grpc.SimulationStub(
            channel=self.channel)

    def ctrl_ping(self, ctrl_ping_request):
        return self.stub.ctrl_ping(ctrl_ping_request)

    def list_model_instances(self, list_model_instances_request):
        return self.stub.list_model_instances(list_model_instances_request)

    def delete_model_instances(self, delete_model_instances_request):
        return self.stub.delete_model_instances(delete_model_instances_request)

    def start_simulation(self, start_simulation_request):
        return self.stub.start_simulation(start_simulation_request)

    def simulation_graph(self, simulation_graph_request):
        return self.stub.simulation_graph(simulation_graph_request)

    def simulation_logs(self, simulation_logs_request):
        return self.stub.simulation_logs(simulation_logs_request)

    def close_simulation(self, close_simulation_request):
        return self.stub.close_simulation(close_simulation_request)
