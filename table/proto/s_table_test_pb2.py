# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2



_TEST = descriptor.Descriptor(
  name='test',
  full_name='table.test',
  filename='s_table_test.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='table.test.id', index=0,
      number=1, type=17, cpp_type=1, label=1,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='num', full_name='table.test.num', index=1,
      number=3, type=2, cpp_type=6, label=1,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_TEST_ARRAY = descriptor.Descriptor(
  name='test_ARRAY',
  full_name='table.test_ARRAY',
  filename='s_table_test.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='rows', full_name='table.test_ARRAY.rows', index=0,
      number=1, type=11, cpp_type=10, label=3,
      default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_TESTA = descriptor.Descriptor(
  name='testa',
  full_name='table.testa',
  filename='s_table_test.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='table.testa.id', index=0,
      number=1, type=17, cpp_type=1, label=1,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='degree_quality_type', full_name='table.testa.degree_quality_type', index=1,
      number=3, type=14, cpp_type=8, label=1,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_TESTA_ARRAY = descriptor.Descriptor(
  name='testa_ARRAY',
  full_name='table.testa_ARRAY',
  filename='s_table_test.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='rows', full_name='table.testa_ARRAY.rows', index=0,
      number=1, type=11, cpp_type=10, label=3,
      default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)

import common_degree_pb2
import common_effect_pb2

_TEST_ARRAY.fields_by_name['rows'].message_type = _TEST
_TESTA.fields_by_name['degree_quality_type'].enum_type = common_degree_pb2._DEGREEQUALITYTYPE
_TESTA_ARRAY.fields_by_name['rows'].message_type = _TESTA

class test(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TEST

class test_ARRAY(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TEST_ARRAY

class testa(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TESTA

class testa_ARRAY(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TESTA_ARRAY

