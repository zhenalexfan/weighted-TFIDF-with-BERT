# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: query.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='query.proto',
  package='query',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0bquery.proto\x12\x05query\"\x1b\n\x05Query\x12\x12\n\nuser_input\x18\x01 \x01(\t\"\x1a\n\x05Reply\x12\x11\n\tsent_type\x18\x01 \x01(\t29\n\tSentQuery\x12,\n\x0cReturnResult\x12\x0c.query.Query\x1a\x0c.query.Reply\"\x00\x62\x06proto3')
)




_QUERY = _descriptor.Descriptor(
  name='Query',
  full_name='query.Query',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_input', full_name='query.Query.user_input', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=22,
  serialized_end=49,
)


_REPLY = _descriptor.Descriptor(
  name='Reply',
  full_name='query.Reply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sent_type', full_name='query.Reply.sent_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=51,
  serialized_end=77,
)

DESCRIPTOR.message_types_by_name['Query'] = _QUERY
DESCRIPTOR.message_types_by_name['Reply'] = _REPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Query = _reflection.GeneratedProtocolMessageType('Query', (_message.Message,), dict(
  DESCRIPTOR = _QUERY,
  __module__ = 'query_pb2'
  # @@protoc_insertion_point(class_scope:query.Query)
  ))
_sym_db.RegisterMessage(Query)

Reply = _reflection.GeneratedProtocolMessageType('Reply', (_message.Message,), dict(
  DESCRIPTOR = _REPLY,
  __module__ = 'query_pb2'
  # @@protoc_insertion_point(class_scope:query.Reply)
  ))
_sym_db.RegisterMessage(Reply)



_SENTQUERY = _descriptor.ServiceDescriptor(
  name='SentQuery',
  full_name='query.SentQuery',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=79,
  serialized_end=136,
  methods=[
  _descriptor.MethodDescriptor(
    name='ReturnResult',
    full_name='query.SentQuery.ReturnResult',
    index=0,
    containing_service=None,
    input_type=_QUERY,
    output_type=_REPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SENTQUERY)

DESCRIPTOR.services_by_name['SentQuery'] = _SENTQUERY

# @@protoc_insertion_point(module_scope)
