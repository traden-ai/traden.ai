import unittest
from constants import PYTHON_PATH
from SimulationContract.generated_files.simulation_pb2 import *
from SimulationTester.main.simulation_frontend import SimulationFrontend

SIMULATION_HOST = "localhost"
SIMULATION_PORT = 8082


class SimulationIT(unittest.TestCase):

    frontend = SimulationFrontend(SIMULATION_HOST, SIMULATION_PORT)

    PING_MESSAGE = "ping"
    MODEL_INSTANCES_PATH = "/Models/instances/"
    MODEL_INSTANCE_NAME = "model_instance_test"

    VALID_MODEL_INSTANCES = ["EMACrossing", "Random"]
    INVALID_MODEL_INSTANCES = ["invalid", "not_model_instance"]

    VALID_START_DATE = "2019-03-01"
    INVALID_START_DATE = "2800-01-01"

    VALID_END_DATE = "2019-06-01"
    INVALID_END_DATE = "2900-01-01"

    VALID_TICKERS = ["NIO", "TLRY"]
    INVALID_TICKERS = ["invalid", "not_ticker"]

    BALANCE = 100000.0
    TRANSACTION_FEE = .0
    NUMBER_EXECUTIONS = 2

    VALID_SIMULATION_ID = 0
    INVALID_SIMULATION_ID = 1000000

    def test_ctrl_ping(self):
        response = self.frontend.ctrl_ping(CtrlPingRequest(input=self.PING_MESSAGE))
        self.assertEqual(response.output, self.PING_MESSAGE)

    def test_list_and_delete_model_instances(self):
        # create a temporary instance
        with open(PYTHON_PATH + self.MODEL_INSTANCES_PATH + self.MODEL_INSTANCE_NAME, 'w') as f:
            f.write(self.MODEL_INSTANCE_NAME)

        response = self.frontend.list_model_instances(ListInstancesRequest())
        self.assertIn(self.MODEL_INSTANCE_NAME, response.instances)

        self.frontend.delete_model_instances(DeleteInstancesRequest(instances=[self.MODEL_INSTANCE_NAME]))
        response = self.frontend.list_model_instances(ListInstancesRequest())
        self.assertNotIn(self.MODEL_INSTANCE_NAME, response.instances)

    def test_start_simulation_unavailable_model_instances(self):
        response = self.frontend.start_simulation(StartSimulationRequest(
            balance=self.BALANCE,
            tickers=self.VALID_TICKERS,
            interval=TimeInterval(
                start_date=self.VALID_START_DATE,
                end_date=self.VALID_END_DATE
            ),
            models=self.INVALID_MODEL_INSTANCES,
            transaction_fee=self.TRANSACTION_FEE,
            number_executions=self.NUMBER_EXECUTIONS
        ))
        self.assertEqual(StartSimulationResponse.Status.MODEL_INSTANCES_NOT_AVAILABLE, response.status)

    def test_start_simulation_unavailable_tickers(self):
        response = self.frontend.start_simulation(StartSimulationRequest(
            balance=self.BALANCE,
            tickers=self.INVALID_TICKERS,
            interval=TimeInterval(
                start_date=self.VALID_START_DATE,
                end_date=self.VALID_END_DATE
            ),
            models=self.VALID_MODEL_INSTANCES,
            transaction_fee=self.TRANSACTION_FEE,
            number_executions=self.NUMBER_EXECUTIONS
        ))
        self.assertEqual(StartSimulationResponse.Status.TICKERS_NOT_AVAILABLE, response.status)

    def test_start_simulation_unavailable_time_interval(self):
        response = self.frontend.start_simulation(StartSimulationRequest(
            balance=self.BALANCE,
            tickers=self.VALID_TICKERS,
            interval=TimeInterval(
                start_date=self.INVALID_START_DATE,
                end_date=self.INVALID_END_DATE
            ),
            models=self.VALID_MODEL_INSTANCES,
            transaction_fee=self.TRANSACTION_FEE,
            number_executions=self.NUMBER_EXECUTIONS
        ))
        self.assertEqual(StartSimulationResponse.Status.INTERVAL_NOT_AVAILABLE, response.status)

    def test_start_simulation_success(self):
        response = self.frontend.start_simulation(StartSimulationRequest(
            balance=self.BALANCE,
            tickers=self.VALID_TICKERS,
            interval=TimeInterval(
                start_date=self.VALID_START_DATE,
                end_date=self.VALID_END_DATE
            ),
            models=self.VALID_MODEL_INSTANCES,
            transaction_fee=self.TRANSACTION_FEE,
            number_executions=self.NUMBER_EXECUTIONS
        ))
        self.assertEqual(StartSimulationResponse.Status.OK, response.status)

    def test_simulation_graph_invalid_id(self):
        _, status = self.frontend.simulation_graph(SimulationGraphRequest(
            simulation_id=self.INVALID_SIMULATION_ID
        ))
        self.assertEqual(SimulationGraphResponse.Status.SIMULATION_NOT_FOUND, status)

    def test_simulation_graph_success(self):
        _, status = self.frontend.simulation_graph(SimulationGraphRequest(
            simulation_id=self.VALID_SIMULATION_ID
        ))
        self.assertEqual(SimulationGraphResponse.Status.OK, status)

    def test_simulation_logs_invalid_id(self):
        _, status = self.frontend.simulation_logs(SimulationLogsRequest(
            simulation_id=self.INVALID_SIMULATION_ID
        ))
        self.assertEqual(SimulationLogsResponse.Status.SIMULATION_NOT_FOUND, status)

    def test_simulation_logs_success(self):
        _, status = self.frontend.simulation_logs(SimulationLogsRequest(
            simulation_id=self.VALID_SIMULATION_ID
        ))
        self.assertEqual(SimulationLogsResponse.Status.OK, status)

    def test_close_simulation_invalid_id(self):
        response = self.frontend.close_simulation(CloseSimulationRequest(
            simulation_id=self.INVALID_SIMULATION_ID
        ))
        self.assertEqual(CloseSimulationResponse.Status.SIMULATION_NOT_FOUND, response.status)

    def test_close_simulation_success(self):
        response = self.frontend.close_simulation(CloseSimulationRequest(
            simulation_id=self.VALID_SIMULATION_ID
        ))
        self.assertEqual(CloseSimulationResponse.Status.OK, response.status)


if __name__ == '__main__':
    unittest.main()
