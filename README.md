# cisco-mdt-python
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

This library provides a basic Model-Driven Telemetry (MDT) server implementation to ease development, as well as a sample CLI potentially useful for debugging.

## Usage
```bash
pip install cisco-mdt
python -c "import cisco_mdt; print(cisco_mdt)"
cisco-mdt --help
```

This library only implements the MDT gRPC server at this time.

### cisco-mdt CLI
A CLI callable as `cisco-mdt` is provided which may be useful for simply interacting with an MDT capable Cisco device, and also serves as a reference for how to use this `cisco_mdt` library. CLI usage is documented at the bottom of this README in [CLI Usage](#cli-usage).

### MDTgRPCServer
A simple implementation of a Cisco MDT server/receiver is provided which allows the library user to specify callback functions on a per-message basis. This allows flexibility in implementation. This class may also be subclassed and the `MdtDialout` method overridden for completely custom control of the incoming requests and context.

#### Examples
`MDTgRPCServer` is used like any gRPC servicer implementation, but with the notion of callbacks.

```python
"""Effectively ripped from cli.py"""
from concurrent import futures
import grpc
from google.protobuf import json_format, text_format
from cisco_mdt import proto, MDTgRPCServer


def callback(request):
    telemetry_pb = proto.telemetry_bis_pb2.Telemetry()
    telemetry_pb.ParseFromString(request.data)
    logging.debug(text_format.MessageToString(request))
    logging.info(text_format.MessageToString(telemetry_pb))

mdt_grpc_server = MDTgRPCServer()
mdt_grpc_server.add_mdt_callback(callback)
grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
proto.mdt_dialout_pb2_grpc.add_gRPCMdtDialoutServicer_to_server(
    mdt_grpc_server, grpc_server
)
grpc_server.add_insecure_port("[::]:50051")
grpc_server.start()
try:
    grpc_server.wait_for_termination()
except KeyboardInterrupt:
    logging.warning("Stopping on interrupt.")
    grpc_server.stop(None)
except Exception:
    logging.exception("Stopping due to exception!")
```

## Model-Driven Telemetry
Model-Driven Telemetry (MDT) is a feature across IOS XE, IOS XR, and NX-OS which may be used to export various operational data sources with general greater efficiency than other similar protocols such as SNMP. MDT has options which vary across operating systems (such as transport, encoding, etc.), but at minimum all platforms provide a "dial-out", "push" model of operation, gRPC client implementation with self-describing protocol buffers which may connect to an implementing gRPC server and export desired data. Generally this data is described via YANG modules, and desired data specified by YANG XPaths.

## Development
Requires Python and utilizes `pipenv` for environment management. Manual usage of `pip`/`virtualenv` is not covered. Uses `black` for code formatting and `pylint` for code linting. `black` is not explicitly installed as it requires Python 3.6+.

### Get Source
```bash
git clone https://github.com/cisco-ie/cisco-mdt-python.git
cd cisco-mdt-python
# If pipenv not installed, install!
pip install --user pipenv
# Now use Makefile...
make setup
# Or pipenv manually if make not present
pipenv --three install --dev
# Enter virtual environment
pipenv shell
# Work work
exit
```

### Code Hygiene
We use [`black`](https://github.com/ambv/black) for code formatting and [`pylint`](https://www.pylint.org/) for code linting. `hygiene.sh` will run `black` against all of the code under `src/cisco_mdt/` except for `protoc` compiled protobufs, and run `pylint` against Python files directly under `gnmi/`. They don't totally agree, so we're not looking for perfection here. `black` is not automatically installed due to requiring Python 3.6+. `hygiene.sh` will check for regular path availability and via `pipenv`, and otherwise falls directly to `pylint`. If `black` usage is desired, please install it into `pipenv` if using Python 3.6+ or separate methods e.g. `brew install black`.

```bash
# If using Python 3.6+
pipenv install --dev black
# Otherwise...
./hygiene.sh
```

### Recompile Protobufs
If new protocol buffer definitions (`proto/`) are released, use `update_protos.sh` to recompile. If breaking changes are introduced the library must be updated.

```bash
./update_protos.sh
```

## CLI Usage
The below details the current `cisco-mdt` usage options.

```
cisco-mdt --help
usage:
cisco-mdt <protocol> [<args>]

Version 0.0.1

Supported Protocols:
grpc

cisco-mdt grpc

See <protocol> --help for RPC options.


MDT CLI demonstrating cisco_mdt library usage.

positional arguments:
  protocol    MDT protocol to utilize.

optional arguments:
  -h, --help  show this help message and exit
```

### gRPC
This protocol will handle MDT via gRPC transport and dump the telemetry data in JSON or textual protocol buffer format to `stdout`.

```
cisco-gnmi grpc -netloc 0.0.0.0:50051 -debug
```

#### Usage
```
cisco-mdt grpc --help
usage: cisco-mdt [-h] [-dump_json] [-netloc NETLOC] [-debug]

Start gRPC protocol server.

optional arguments:
  -h, --help      show this help message and exit
  -dump_json      Dump as JSON instead of textual protos.
  -netloc NETLOC  <host>:<port>
  -debug          Print debug messages.
```

#### Output
```
[cisco-mdt-python] cisco-mdt grpc -debug
DEBUG:root:Starting gRPC server on [::]:50051.
DEBUG:root:ReqId: 10
data: "\n\003ios\032\006testme29openconfig-interfaces:interfaces/..."

INFO:root:node_id_str: "ios"
subscription_id_str: "testme"
encoding_path: "openconfig-interfaces:interfaces/interface/state/counters"
collection_id: 914301
...
```

## Licensing
`cisco-mdt-python` is licensed as [Apache License, Version 2.0](LICENSE).

## Issues
Open an issue :)

## Related Projects
1. [YangModels/yang](https://github.com/YangModels/yang)
2. [cisco-ie/cisco-proto](https://github.com/cisco-ie/cisco-proto)
3. [CiscoDevNet/nx-telemetry-proto](https://github.com/CiscoDevNet/nx-telemetry-proto)
4. [ios-xr/model-driven-telemetry](https://github.com/ios-xr/model-driven-telemetry)
5. [Telegraf Cisco MDT Plugin](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/cisco_telemetry_mdt)
6. [Pipeline](https://github.com/cisco/bigmuddy-network-telemetry-pipeline)