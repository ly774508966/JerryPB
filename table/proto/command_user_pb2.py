# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
_CMD = descriptor.EnumDescriptor(
  name='CMD',
  full_name='Cmd.User.CMD',
  filename='CMD',
  values=[
    descriptor.EnumValueDescriptor(
      name='CMD_INVALID', index=0, number=65535,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='CMD_BUY_ARENA_SHOP_GOODS_REQ', index=1, number=10626,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='CMD_BUY_ARENA_SHOP_GOODS_RSP', index=2, number=10627,
      options=None,
      type=None),
  ],
  options=None,
)


_RET = descriptor.EnumDescriptor(
  name='RET',
  full_name='Cmd.User.RET',
  filename='RET',
  values=[
    descriptor.EnumValueDescriptor(
      name='RET_SYS_ERR', index=0, number=-1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='RET_SUCCESS', index=1, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='RET_MODULE_SWITCH_OFF', index=2, number=256,
      options=None,
      type=None),
  ],
  options=None,
)


CMD_INVALID = 65535
CMD_BUY_ARENA_SHOP_GOODS_REQ = 10626
CMD_BUY_ARENA_SHOP_GOODS_RSP = 10627
RET_SYS_ERR = -1
RET_SUCCESS = 0
RET_MODULE_SWITCH_OFF = 256




