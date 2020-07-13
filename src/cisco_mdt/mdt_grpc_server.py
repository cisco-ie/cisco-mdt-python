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

"""Basic implementation of gRPC server able to receive MDT messages.
This server should either be subclassed to override the MdtDialout method
or should call add_mdt_callback to provide callback methods to an instance
for processing per message.
"""
from threading import Lock

from . import proto


class MDTgRPCServer(proto.mdt_dialout_pb2_grpc.gRPCMdtDialoutServicer):
    """MDT gRPC server implementation with basic callback implementation.
    MdtDialout method may be overridden by subclasses for custom parsing.

    Methods
    -------
    add_mdt_callback(...)
        Adds a callback to be called per MDT message.
    remove_mdt_callback(...)
        Removes a previously added callback.
    MdtDialout(...)
        This method is the singular server RPC receiver, calls callbacks
        per message. Override for more custom parsing.
    """

    def __init__(self):
        self.__callbacks = set()
        self.__callbacks_mutex = Lock()

    def add_mdt_callback(self, callback):
        """Adds a callback function to be called per MDT message.

        Parameters
        ----------
        callback : function
            A function which will be called with the MDT request
            protobuf message when received.
        """
        with self.__callbacks_mutex:
            self.__callbacks.add(callback)

    def remove_mdt_callback(self, callback):
        """Removes the callback function to be called per MDT message.

        Parameters
        ----------
        callback : function
            The function previously specified to be added for MDT callback.
        """
        with self.__callbacks_mutex:
            self.__callbacks.remove(callback)

    def MdtDialout(self, request_iterator, context):
        for request in request_iterator:
            with self.__callbacks_mutex:
                for callback in self.__callbacks:
                    callback(request)
            yield proto.mdt_dialout_pb2.MdtDialoutArgs(ReqId=request.ReqId)
