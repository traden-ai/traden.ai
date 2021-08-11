import os

from constants import PYTHON_PATH

CONTRACTS = {
    ("DataProviderContract", "data_provider"),
    ("SimulationContract", "simulation"),
    ("ExchangeContract", "exchange")
}

if __name__ == '__main__':
    code = ""
    for directory, name in CONTRACTS:
        path = PYTHON_PATH + "/" + directory
        if not os.path.isdir(path + "/generated_files/"):
            os.mkdir(path + "/generated_files/")
        os.system(f"python3 -m grpc_tools.protoc -I. --python_out={path}/generated_files/" +
                  f" --grpc_python_out={path}/generated_files/ --proto_path={path}/ {name}.proto")
        with open(path + f"/generated_files/{name}_pb2_grpc.py", 'r') as f:
            code = f.read()
        with open(path + f"/generated_files/{name}_pb2_grpc.py", 'w') as f:
            f.write(code.replace(f"import {name}_pb2", f"import {directory}.generated_files.{name}_pb2"))
