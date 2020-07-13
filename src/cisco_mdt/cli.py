"""Copyright 2020 Cisco Systems
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

 * Redistributions of source code must retain the above copyright
 notice, this list of conditions and the following disclaimer.

The contents of this file are licensed under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
"""

"""Basic CLI to demonstrate usage of library and provide some out of box
usability for MDT visibility.
"""
import sys
import argparse
import logging
from concurrent import futures
import grpc
from google.protobuf import json_format, text_format


from . import MDTgRPCServer
from . import proto
from . import __version__

# Stopgap to easily tell callback how to format output
__dump_as_json = False


def cli_mdt_callback(request):
    """A basic callback for the MDTgRPCServer instance which parses
    telemetry data and dumps the entire request to DEBUG and the
    telemetry data itself as INFO.
    """
    telemetry_pb = proto.telemetry_bis_pb2.Telemetry()
    telemetry_pb.ParseFromString(request.data)
    logging.debug(__format_message(request, __dump_as_json))
    logging.info(__format_message(telemetry_pb, __dump_as_json))


def main():
    """CLI entrypoint."""
    protocol_map = {"grpc": mdt_grpc}
    parser = argparse.ArgumentParser(
        description="MDT CLI demonstrating cisco_mdt library usage.",
        usage="""
cisco-mdt <protocol> [<args>]

Version {version}

Supported Protocols:
{supported_protocols}

cisco-mdt grpc

See <protocol> --help for RPC options.
    """.format(
            version=__version__,
            supported_protocols="\n".join(sorted(list(protocol_map.keys()))),
        ),
    )
    parser.add_argument("protocol", help="MDT protocol to utilize.")
    args = parser.parse_args(sys.argv[1:2])
    if args.protocol not in protocol_map.keys():
        logging.error(
            "%s not in supported protocols: %s!",
            args.protocol,
            ", ".join(protocol_map.keys()),
        )
        parser.print_help()
        sys.exit(1)
    try:
        protocol_map[args.protocol]()
    except Exception:
        logging.exception("Error during usage!")
        sys.exit(2)


def mdt_grpc():
    """MDT gRPC CLI implementation."""
    parser = argparse.ArgumentParser(description="Start gRPC protocol server.")
    parser.add_argument(
        "-dump_json",
        help="Dump as JSON instead of textual protos.",
        action="store_true",
    )
    args = __common_args_handler(parser)
    global __dump_as_json
    __dump_as_json = args.dump_json
    mdt_grpc_server = MDTgRPCServer()
    mdt_grpc_server.add_mdt_callback(cli_mdt_callback)
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    proto.mdt_dialout_pb2_grpc.add_gRPCMdtDialoutServicer_to_server(
        mdt_grpc_server, grpc_server
    )
    grpc_server.add_insecure_port(args.netloc)
    logging.debug("Starting gRPC server on %s.", args.netloc)
    grpc_server.start()
    try:
        grpc_server.wait_for_termination()
    except KeyboardInterrupt:
        logging.warning("Stopping on interrupt.")
        grpc_server.stop(None)
    except Exception:
        logging.exception("Stopping due to exception!")


def __format_message(message, as_json=False):
    """Formats a protobuf message as either text_format or json_format.

    Parameters
    ----------
    message : protobuf
        The protobuf message to decode.
    as_json : bool
        Dump as JSON instead of protobuf text format when True.

    Returns
    -------
    formatted_msg : str
    """
    formatted_message = None
    if as_json:
        formatted_message = json_format.MessageToJson(message, sort_keys=True)
    else:
        formatted_message = text_format.MessageToString(message)
    return formatted_message


def __common_args_handler(parser):
    """Handle common arguments per protocol function.
    Ideally would be a decorator.
    """
    parser.add_argument("-netloc", help="<host>:<port>", default="[::]:50051", type=str)
    parser.add_argument("-debug", help="Print debug messages.", action="store_true")
    args = parser.parse_args(sys.argv[2:])
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    return args
