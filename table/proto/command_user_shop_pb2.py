# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2



_BUY_ARENA_SHOP_GOODS_REQ = descriptor.Descriptor(
  name='BUY_ARENA_SHOP_GOODS_REQ',
  full_name='Cmd.User.BUY_ARENA_SHOP_GOODS_REQ',
  filename='command_user_shop.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='idx', full_name='Cmd.User.BUY_ARENA_SHOP_GOODS_REQ.idx', index=0,
      number=1, type=13, cpp_type=3, label=1,
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


_BUY_ARENA_SHOP_GOODS_RSP = descriptor.Descriptor(
  name='BUY_ARENA_SHOP_GOODS_RSP',
  full_name='Cmd.User.BUY_ARENA_SHOP_GOODS_RSP',
  filename='command_user_shop.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='goods_list', full_name='Cmd.User.BUY_ARENA_SHOP_GOODS_RSP.goods_list', index=0,
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

import common_shop_pb2

_BUY_ARENA_SHOP_GOODS_RSP.fields_by_name['goods_list'].message_type = common_shop_pb2._ARENASHOP_GOODS

class BUY_ARENA_SHOP_GOODS_REQ(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BUY_ARENA_SHOP_GOODS_REQ

class BUY_ARENA_SHOP_GOODS_RSP(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BUY_ARENA_SHOP_GOODS_RSP

