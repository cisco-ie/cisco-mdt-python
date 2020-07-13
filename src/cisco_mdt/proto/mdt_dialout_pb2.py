# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mdt_dialout.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mdt_dialout.proto',
  package='mdt_dialout',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11mdt_dialout.proto\x12\x0bmdt_dialout\"P\n\x0eMdtDialoutArgs\x12\r\n\x05ReqId\x18\x01 \x01(\x03\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x12\x0e\n\x06\x65rrors\x18\x03 \x01(\t\x12\x11\n\ttotalSize\x18\x04 \x01(\x05\x32^\n\x0egRPCMdtDialout\x12L\n\nMdtDialout\x12\x1b.mdt_dialout.MdtDialoutArgs\x1a\x1b.mdt_dialout.MdtDialoutArgs\"\x00(\x01\x30\x01\x62\x06proto3'
)




_MDTDIALOUTARGS = _descriptor.Descriptor(
  name='MdtDialoutArgs',
  full_name='mdt_dialout.MdtDialoutArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ReqId', full_name='mdt_dialout.MdtDialoutArgs.ReqId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='mdt_dialout.MdtDialoutArgs.data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='errors', full_name='mdt_dialout.MdtDialoutArgs.errors', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='totalSize', full_name='mdt_dialout.MdtDialoutArgs.totalSize', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=34,
  serialized_end=114,
)

DESCRIPTOR.message_types_by_name['MdtDialoutArgs'] = _MDTDIALOUTARGS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MdtDialoutArgs = _reflection.GeneratedProtocolMessageType('MdtDialoutArgs', (_message.Message,), {
  'DESCRIPTOR' : _MDTDIALOUTARGS,
  '__module__' : 'mdt_dialout_pb2'
  # @@protoc_insertion_point(class_scope:mdt_dialout.MdtDialoutArgs)
  })
_sym_db.RegisterMessage(MdtDialoutArgs)



_GRPCMDTDIALOUT = _descriptor.ServiceDescriptor(
  name='gRPCMdtDialout',
  full_name='mdt_dialout.gRPCMdtDialout',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=116,
  serialized_end=210,
  methods=[
  _descriptor.MethodDescriptor(
    name='MdtDialout',
    full_name='mdt_dialout.gRPCMdtDialout.MdtDialout',
    index=0,
    containing_service=None,
    input_type=_MDTDIALOUTARGS,
    output_type=_MDTDIALOUTARGS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_GRPCMDTDIALOUT)

DESCRIPTOR.services_by_name['gRPCMdtDialout'] = _GRPCMDTDIALOUT

# @@protoc_insertion_point(module_scope)
