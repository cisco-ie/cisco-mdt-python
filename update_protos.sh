#!/usr/bin/env bash
echo "Updating proto sources ..."
cp proto/*.proto src/cisco_mdt/proto/
echo "Compiling protos ..."
pipenv run python -m grpc_tools.protoc --proto_path=src/cisco_mdt/proto --python_out=src/cisco_mdt/proto --grpc_python_out=src/cisco_mdt/proto mdt_dialout.proto telemetry_bis.proto
echo "Fixing compiled Python imports ..."
python -c "
with open('src/cisco_mdt/proto/mdt_dialout_pb2_grpc.py', 'r') as proto_fd:
  file_content = proto_fd.read()
file_content = file_content.replace('import mdt_dialout_pb2', 'from . import mdt_dialout_pb2', 1)
with open('src/cisco_mdt/proto/mdt_dialout_pb2_grpc.py', 'w') as proto_fd:
  proto_fd.write(file_content)
"
echo "Cleaning up ..."
rm src/cisco_mdt/proto/*.proto