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
    TRANSACTION_FEE = .01
    NUMBER_EXECUTIONS = 2

    VALID_SIMULATION_ID = 0
    INVALID_SIMULATION_ID = 1000000

    def test_a_ctrl_ping(self):
        request = CtrlPingRequest(input=self.PING_MESSAGE)
        response = self.frontend.ctrl_ping(request)
        self.assertEqual(response.output, self.PING_MESSAGE)

    def test_b_list_and_delete_model_instances(self):
        # create a temporary instance
        with open(PYTHON_PATH + self.MODEL_INSTANCES_PATH + self.MODEL_INSTANCE_NAME, 'w') as f:
            f.write(self.MODEL_INSTANCE_NAME)

        request = ListInstancesRequest()
        response = self.frontend.list_model_instances(request)
        self.assertIn(self.MODEL_INSTANCE_NAME, response.instances)

        request = DeleteInstancesRequest(instances=[self.MODEL_INSTANCE_NAME])
        self.frontend.delete_model_instances(request)

        request = ListInstancesRequest()
        response = self.frontend.list_model_instances(request)
        self.assertNotIn(self.MODEL_INSTANCE_NAME, response.instances)

    def test_c_start_simulation_unavailable_model_instances(self):
        request = StartSimulationRequest(
            balance=self.BALANCE,
            tickers=self.VALID_TICKERS,
            interval=TimeInterval(
                start_date=self.VALID_START_DATE,
                end_date=self.VALID_END_DATE
            ),
            models=self.INVALID_MODEL_INSTANCES,
            transaction_fee=self.TRANSACTION_FEE,
            number_executions=self.NUMBER_EXECUTIONS
        )
        response = self.frontend.start_simulation(request)
        self.assertEqual(StartSimulationResponse.Status.MODEL_INSTANCES_NOT_AVAILABLE, response.status)

    def test_d_start_simulation_unavailable_tickers(self):
        request = StartSimulationRequest(
            balance=self.BALANCE,
            tickers=self.INVALID_TICKERS,
            interval=TimeInterval(
                start_date=self.VALID_START_DATE,
                end_date=self.VALID_END_DATE
            ),
            models=self.VALID_MODEL_INSTANCES,
            transaction_fee=self.TRANSACTION_FEE,
            number_executions=self.NUMBER_EXECUTIONS
        )
        response = self.frontend.start_simulation(request)
        self.assertEqual(StartSimulationResponse.Status.TICKERS_NOT_AVAILABLE, response.status)

    def test_e_start_simulation_unavailable_time_interval(self):
        request = StartSimulationRequest(
            balance=self.BALANCE,
            tickers=self.VALID_TICKERS,
            interval=TimeInterval(
                start_date=self.INVALID_START_DATE,
                end_date=self.INVALID_END_DATE
            ),
            models=self.VALID_MODEL_INSTANCES,
            transaction_fee=self.TRANSACTION_FEE,
            number_executions=self.NUMBER_EXECUTIONS
        )
        response = self.frontend.start_simulation(request)
        self.assertEqual(StartSimulationResponse.Status.INTERVAL_NOT_AVAILABLE, response.status)

    def test_f_start_simulation_success(self):
        request = StartSimulationRequest(
            balance=self.BALANCE,
            tickers=self.VALID_TICKERS,
            interval=TimeInterval(
                start_date=self.VALID_START_DATE,
                end_date=self.VALID_END_DATE
            ),
            models=self.VALID_MODEL_INSTANCES,
            transaction_fee=self.TRANSACTION_FEE,
            number_executions=self.NUMBER_EXECUTIONS
        )
        response = self.frontend.start_simulation(request)
        self.assertEqual(StartSimulationResponse.Status.OK, response.status)
        self.VALID_SIMULATION_ID = response.simulation_result.simulation_id

    def test_g_simulation_graph_invalid_id(self):
        request = SimulationGraphRequest(
            simulation_id=self.INVALID_SIMULATION_ID
        )
        _, status = self.frontend.simulation_graph(request)
        self.assertEqual(SimulationGraphResponse.Status.SIMULATION_NOT_FOUND, status)

    def test_h_simulation_graph_success(self):
        request = SimulationGraphRequest(
            simulation_id=self.VALID_SIMULATION_ID
        )
        _, status = self.frontend.simulation_graph(request)
        self.assertEqual(SimulationGraphResponse.Status.OK, status)

    def test_i_simulation_logs_invalid_id(self):
        request = SimulationLogsRequest(
            simulation_id=self.INVALID_SIMULATION_ID
        )
        _, status = self.frontend.simulation_logs(request)
        self.assertEqual(SimulationLogsResponse.Status.SIMULATION_NOT_FOUND, status)

    def test_j_simulation_logs_success(self):
        request = SimulationLogsRequest(
            simulation_id=self.VALID_SIMULATION_ID
        )
        _, status = self.frontend.simulation_logs(request)
        self.assertEqual(SimulationLogsResponse.Status.OK, status)

    def test_k_close_simulation_invalid_id(self):
        request = CloseSimulationRequest(
            simulation_id=self.INVALID_SIMULATION_ID
        )
        response = self.frontend.close_simulation(request)
        self.assertEqual(CloseSimulationResponse.Status.SIMULATION_NOT_FOUND, response.status)

    def test_l_close_simulation_success(self):
        request = CloseSimulationRequest(
            simulation_id=self.VALID_SIMULATION_ID
        )
        response = self.frontend.close_simulation(request)
        self.assertEqual(CloseSimulationResponse.Status.OK, response.status)


if __name__ == '__main__':
    unittest.main()
