#!/usr/bin/python
# encoding=utf-8
#==================================================#
#   Excel表格数据 -> 二进制数据转换工具。          #
#   Powered By 赵广宇, michaelpublic@qq.com        #    
#--------------------------------------------------#
#   Copyright © 2014 赵广宇. All Rights Reserved.  #
#==================================================#

import os
import re
import sys
import xlrd
import google
import traceback
from datetime import datetime
from logger import Logger

DEBUG_MODE = False

logger = Logger(Logger.LEVEL_ERROR, 'table_tools')

#================================================#
#################### 配置模块 ####################
#================================================#
class Config(object):
    def __init__(self):
        # 单表最大字段数
        self.max_field_number = 99

        # 全局的位置定义
        self.workbook_dir           = '../table'
        self.proto_dir              = '../proto'
        self.output_dir             = '../output/table_data'
        self.default_proto_prefix   = 'c_table_'
        self.default_output_prefix  = ''
        self.default_output_suffix  = 'bytes'

        if os.environ.get('WORKBOOK_DIR') != None:
            self.workbook_dir = os.environ.get('WORKBOOK_DIR')

        if os.environ.get('PROTO_DIR') != None:
            self.proto_dir = os.environ.get('PROTO_DIR')

        if os.environ.get('OUTPUT_DIR') != None:
            self.output_dir = os.environ.get('OUTPUT_DIR')

        if os.environ.get('DEFAULT_PROTO_PREFIX') != None:
            self.default_proto_prefix = os.environ.get('DEFAULT_PROTO_PREFIX');

        if os.environ.get('DEFAULT_OUTPUT_PREFIX') != None:
            self.default_output_prefix = os.environ.get('DEFAULT_OUTPUT_PREFIX');

        if os.environ.get('DEFAULT_OUTPUT_SUFFIX') != None:
            self.default_output_suffix = os.environ.get('DEFAULT_OUTPUT_SUFFIX');

        #logger.info('Environs: WORKBOOK_DIR = \'%s\'' % self.workbook_dir)
        #logger.info('Environs: PROTO_DIR = \'%s\'' % self.proto_dir)
        #logger.info('Environs: OUTPUT_DIR = \'%s\'' % self.output_dir)
        #logger.info('Environs: DEFAULT_PROTO_PREFIX = \'%s\'' % self.default_proto_prefix)
        #logger.info('Environs: DEFAULT_OUTPUT_PREFIX = \'%s\'' % self.default_output_prefix)
        #logger.info('Environs: DEFAULT_OUTPUT_SUFFIX = \'%s\'' % self.default_output_suffix)

config = Config()

#================================================#
#################### 中文提取 ####################
#================================================#
class ChinesePicker(object):
    def __init__(self):
        # for client
        if config.default_proto_prefix == 'c_table_':
            self.f = open(config.output_dir + '/' + 'chinese.txt', 'a')
        else:
            self.f = None

    def check_contain_chinese(self, text):
        if type(text) == str:
            text = text.decode('utf8')
        if type(text) != unicode:
            return False
        pattern = re.compile(u'[\u4e00-\u9fa5]+')
        match = pattern.search(text)
        return True if match else False

    def set_workbook_name(self, name):
        self.workbook_name = name

    def pick(self, text, name):
        if self.f and self.check_contain_chinese(text):
            self.f.write(text.encode('utf8') + '\t' + name + '\t' + self.workbook_name + '\n')

chinese_picker = ChinesePicker()

#================================================#
#################### 处理模块 ####################
#================================================#
class TableWriter(object):

    def __init__(self, workbook, sheet, pb2, array):
        chinese_picker.set_workbook_name(workbook)

        # 打开工作表
        try:
            path = config.workbook_dir + '/' + workbook + '.xlsx'
            self.workbook = xlrd.open_workbook(path)
        except IOError:
            path = config.workbook_dir + '/' + workbook + '.xls'
            self.workbook = xlrd.open_workbook(path)
        #logger.info('打开工作簿|%s' % workbook)

        # 打开页签
        if type(sheet) == int or (type(sheet) == str and sheet.isdigit()):
            self.sheet = self.workbook.sheet_by_index(int(sheet))
        elif type(sheet) == str:
            self.sheet = self.workbook.sheet_by_name(sheet)
        else:
            raise TypeError, '工作簿页签参数类型错误'
        #logger.info('加载页签|%s' % self.sheet.name.encode('utf8'))

        # 加载PB协议模块
        if config.proto_dir not in sys.path:
            sys.path.append(config.proto_dir)
        self.pb2 = __import__(pb2)
        #logger.info('导入PB协议|%s' % pb2)

        # 表格行存储
        self.row_array = getattr(self.pb2, array)()

        # 表格行描述
        self.row_descriptor = self.row_array.rows._message_descriptor

    def __call__(self, output):
        # 遍历表格处理数据
        for nrow in xrange(self.sheet.nrows):
            if nrow < 4:
                continue

            row_values = self.sheet.row_values(nrow)
            if unicode(row_values[0]).strip() == '':
                continue

            if DEBUG_MODE:
                self.deal_row_values(row_values)
            else:
                try:
                    self.deal_row_values(row_values)
                except Exception, e:
                    logger.error(traceback.format_exc())
                    logger.error('处理行数据失败|%d' % nrow)
                    raise e

        # 写入文件
        f = open(config.output_dir + '/' + output, 'wb')
        f.write('TBL' + self.row_array.SerializeToString())
        f.close()

    def deal_row_values(self, row_values):
        #logger.info('处理行数据|%s' % str(row_values))

        row = self.row_array.rows.add()
        for descriptor in self.row_descriptor.fields:
            if descriptor.number > config.max_field_number:
                continue

            value = row_values[descriptor.number - 1]
            # 全部转成unicode进行后续处理
            if type(value) == str:
                value = value.decode('utf8')
            # 空字段不处理
            if type(value) == unicode and len(value.strip()) == 0:
                continue

            if DEBUG_MODE:
                self.deal_field_value(row, descriptor, value)
            else:
                try:
                    self.deal_field_value(row, descriptor, value)
                except Exception, e:
                    logger.error(traceback.format_exc())
                    logger.error('处理字段数据失败|%s|%s|%d' % \
                            (value.encode('utf8'), \
                            descriptor.name, \
                            descriptor.number))
                    raise e

        print row
        #logger.info(row)
        #logger.info('行数据处理结果\n%s' % str(row))

    def deal_field_value(self, row, descriptor, value):
        if descriptor.type != descriptor.TYPE_MESSAGE:
            # 解析简单数据
            if descriptor.label == descriptor.LABEL_REPEATED:
                if type(value) == str or type(value) == unicode:
                    for section in value.strip().split('|'):
                        getattr(row, descriptor.name).append(self.type_cast(descriptor, section.strip()))
                        chinese_picker.pick(section, descriptor.name)
                else:
                    getattr(row, descriptor.name).append(self.type_cast(descriptor, value))
            else:
                setattr(row, descriptor.name, self.type_cast(descriptor, value))
                chinese_picker.pick(value, descriptor.name)
        else:
            # 解析结构化数据
            if descriptor.label == descriptor.LABEL_REPEATED:
                for struct_expr in value.split('|'):
                    self.deal_struct(getattr(row, descriptor.name).add(), struct_expr)
            else:
                self.deal_struct(getattr(row, descriptor.name), value)

    def deal_struct(self, struct, value):
        #logger.info('解析结构|%s' % value.encode('utf8'))

        value = value.strip()

        if re.match('\{[^\^]*(\^[^\^]*)*\}', value) == None:
            raise ValueError, '结构表达式错误|%s' % value.encode('utf8')

        fields = value[1:-1].split('^')

        for descriptor in struct.DESCRIPTOR.fields:
            if descriptor.number > len(fields) or descriptor.number > config.max_field_number:
                continue

            field_value = fields[descriptor.number - 1]
            if len(field_value.strip()) == 0:
                continue

            if descriptor.label == descriptor.LABEL_REPEATED:
                for i in xrange(descriptor.number - 1, len(fields)):
                    getattr(struct, descriptor.name).append(self.type_cast(descriptor, fields[i]))
                    chinese_picker.pick(fields[i], descriptor.name)
            else:
                setattr(struct, descriptor.name, self.type_cast(descriptor, field_value))
                chinese_picker.pick(field_value, descriptor.name)

    @staticmethod
    def type_cast(descriptor, value):
        FLOAT_TYPE = (
                descriptor.TYPE_DOUBLE,
                descriptor.TYPE_FLOAT,
                )
        LONG_TYPE = (
                descriptor.TYPE_INT32,
                descriptor.TYPE_INT64,
                descriptor.TYPE_SINT32,
                descriptor.TYPE_SINT64,
                descriptor.TYPE_UINT32,
                descriptor.TYPE_UINT64,
                descriptor.TYPE_FIXED32,
                descriptor.TYPE_FIXED64,
                descriptor.TYPE_SFIXED32,
                descriptor.TYPE_SFIXED64,
                descriptor.TYPE_ENUM,
                )
        BOOL_TYPE = (
                descriptor.TYPE_BOOL,
                )
        STR_TYPE = (
                descriptor.TYPE_BYTES,
                descriptor.TYPE_STRING,
                )

        if descriptor.type in FLOAT_TYPE:
            if type(value) == unicode or type(value) == str:
                return float(value) if len(value) else 0.0
            else:
                return float(value)
        elif descriptor.type in LONG_TYPE:
            if type(value) == unicode or type(value) == str:
                return long(value) if len(value) else 0
            else:
                return long(value)
        elif descriptor.type in BOOL_TYPE:
            return bool(value)
        elif descriptor.type in STR_TYPE:
            if type(value) == float and value == int(value):
                value = int(value)
            if type(value) != str and type(value) != unicode:
                return str(value)
            return value
        else:
            raise TypeError, 'PB字段类型无法转换'

def Usage(arg0):
    print 'Assuming xls file named \"Workbook.xls\"'
    print arg0 + ' Workbook.xls [Other Optional Args]'
    print '  Arg    Description                             Default'
    print '  -s     sheet index(int) or sheet name(string)  [0]'
    print '  -p     proto compiled pb2 file name            [table_workbook_pb2.py]'
    print '  -m     row message type                        [WORKBOOK]'
    print '  -a     row array message type                  [WORKBOOK_ARRAY]'
    print '  -o     output tbl file name                    [workbook.tbl]'

# 解析参数
def ParseArg(argv):
    if len(argv) < 2:
        return False, None

    workbook = None
    sheet = None
    proto = None
    proto_message = None
    proto_message_array = None
    output = None

    idx = 1
    while idx < len(argv):

        arg = argv[idx]

        if arg == '-s':
            if sheet != None:
                return False, None
            idx += 1; sheet = argv[idx]

        elif arg == '-p':
            if proto != None:
                return False, None
            idx += 1; proto = argv[idx] + '_pb2'

        elif arg == '-m':
            if proto_message != None:
                return False, None
            idx += 1; proto_message = argv[idx]

        elif arg == '-a':
            if proto_message_array != None:
                return False, None
            idx += 1; proto_message_array = argv[idx]

        elif arg == '-o':
            if output != None:
                return False, None
            idx += 1; output = argv[idx] + '.' + config.default_output_suffix

        else:
            if workbook != None:
                return False, None
            workbook = arg

        idx += 1

    if workbook == None:
        return False, None

    if sheet == None:
        sheet = 0

    if proto == None:
        proto = config.default_proto_prefix + workbook.lower() + '_pb2'

    if proto_message == None:
        proto_message = workbook.upper()

    if proto_message_array == None:
        proto_message_array = proto_message + '_ARRAY'

    if output == None:
        output = config.default_output_prefix + workbook.lower() + '.' + config.default_output_suffix

    #workbook = workbook + '.xls'

    return True, (workbook, sheet, proto, proto_message_array, output)

if __name__ == '__main__':
    
    if not os.path.exists(config.output_dir):
        os.makedirs(config.output_dir)

    success, args = ParseArg(sys.argv)
    if not success:
        Usage(sys.argv[0])
        exit(-1)

    #print '======================================================='
    print '******************** Dumping Table ********************'
    #print '======================================================='

    logger.info('Arguments: ' + str(args))
    TableWriter(*args[:-1])(args[-1])
    
