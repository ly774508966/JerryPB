#!/usr/bin/python
# encoding=utf-8

import sys, os, Queue, threading, time
import xlrd
from logger import Logger
from myTable import MyTable, MyTableTool
from config import Config

config = Config()
logger = Logger(Logger.LEVEL_INFO, 'table_tools')

que_table_path = Queue.Queue()
que_to_data = Queue.Queue()
que_to_cs = Queue.Queue()
que_modify_cs = Queue.Queue()

tables = []

class TaskInfo():
    def __init__(self, table, use_type):
        self.table = table
        self.use_type = use_type

def ParseArg(argv):
    if len(argv) < 1:
        return False, None
    return True, argv

def Usage():
    print 'this is Usage()'

def DeleteFile(path, pattern1, pattern2 = ''):
    list = os.listdir(path)
    for line in list:
        file_path = path + '\\' + line
        if os.path.isdir(file_path):
            continue
        if line.find(pattern1) != -1:
            if pattern2 != '':
                if line.find(pattern2) != -1:
                    os.remove(file_path)
            else:
                os.remove(file_path)

def CleanProto(use_typ):
    if use_type == MyTableTool.USE_TYPE_ALL:
        DeleteFile(config.proto_path, '_table_', '.proto')
    elif use_type == MyTableTool.USE_TYPE_CLIENT:
        DeleteFile(config.proto_path, config.client_table_prefix, '.proto')
    elif use_type == MyTableTool.USE_TYPE_SERVER:
        DeleteFile(config.proto_path, config.server_table_prefix, '.proto')

def CleanOutput(use_type):
    if use_type == MyTableTool.USE_TYPE_ALL:
        DeleteFile(config.table_cs_path, '.cs')
        DeleteFile(config.table_data_path, '.tbl')
    elif use_type == MyTableTool.USE_TYPE_CLIENT:
        DeleteFile(config.table_cs_path, '.cs', config.client_table_prefix)
        DeleteFile(config.table_data_path, '.tbl', config.client_table_prefix)
    elif use_type == MyTableTool.USE_TYPE_SERVER:
        DeleteFile(config.table_cs_path, '.cs', config.server_table_prefix)
        DeleteFile(config.table_data_path, '.tbl', config.server_table_prefix)
    
def FindTables(use_type, run_id):
    list = os.listdir(config.table_path)
    for filename in list:
        if filename.find('.xlsx') != -1:
            if run_id == 0:
                table = MyTable(config.table_path + '\\' + filename)
                if use_type == MyTableTool.USE_TYPE_CLIENT or use_type == MyTableTool.USE_TYPE_ALL:
                    table.to_proto(MyTableTool.USE_TYPE_CLIENT)
                if use_type == MyTableTool.USE_TYPE_SERVER or use_type == MyTableTool.USE_TYPE_ALL:
                    table.to_proto(MyTableTool.USE_TYPE_SERVER)
                tables.append(table)
            else:
                que_table_path.put(config.table_path + '\\' + filename)

class ThreadHandleTable(threading.Thread):
    F_PROTO = 0
    F_CS    = 1
    F_ALL   = 2
    
    def __init__(self, use_type, flag, que, que2):
        threading.Thread.__init__(self)
        self.use_type = use_type
        self.flag = flag
        self.que = que
        self.que2 = que2

    def run(self):
        while True:
            if self.flag == self.F_PROTO:
                data = self.que.get()
                table = MyTable(data)
                if self.use_type == MyTableTool.USE_TYPE_CLIENT or self.use_type == MyTableTool.USE_TYPE_ALL:
                    table.to_proto(MyTableTool.USE_TYPE_CLIENT)
                if self.use_type == MyTableTool.USE_TYPE_SERVER or self.use_type == MyTableTool.USE_TYPE_ALL:
                    table.to_proto(MyTableTool.USE_TYPE_SERVER)
                    
                if self.use_type == MyTableTool.USE_TYPE_CLIENT or self.use_type == MyTableTool.USE_TYPE_ALL:
                    que_to_cs.put(TaskInfo(table, MyTableTool.USE_TYPE_CLIENT))
                    que_modify_cs.put(TaskInfo(table, MyTableTool.USE_TYPE_CLIENT))
                if self.use_type == MyTableTool.USE_TYPE_SERVER or self.use_type == MyTableTool.USE_TYPE_ALL:
                    que_to_cs.put(TaskInfo(table, MyTableTool.USE_TYPE_SERVER))
                    que_modify_cs.put(TaskInfo(table, MyTableTool.USE_TYPE_SERVER))

                if self.use_type == MyTableTool.USE_TYPE_CLIENT or self.use_type == MyTableTool.USE_TYPE_ALL:
                    que_to_data.put(TaskInfo(table, MyTableTool.USE_TYPE_CLIENT))
                if self.use_type == MyTableTool.USE_TYPE_SERVER or self.use_type == MyTableTool.USE_TYPE_ALL:
                    que_to_data.put(TaskInfo(table, MyTableTool.USE_TYPE_SERVER))
                    
                self.que.task_done()
            elif self.flag == self.F_CS:
                data = self.que.get()
                data.table.to_cs(data.use_type)
                self.que.task_done()
            elif self.flag == self.F_ALL:
                if self.que.empty() == False:
                    data = self.que.get()
                    data.table.to_data(data.use_type)
                    self.que.task_done()
                else:
                    data = self.que2.get()
                    data.table.modify_cs(data.use_type)
                    self.que2.task_done()
            else:
                continue
            
def RunSync(use_type):
    CleanOutput(use_type)
    FindTables(use_type, 0)

    work_path = os.getcwd()
    os.chdir(config.proto_path)
    for t in tables:
        if use_type == MyTableTool.USE_TYPE_CLIENT or use_type == MyTableTool.USE_TYPE_ALL:
            t.to_cs(MyTableTool.USE_TYPE_CLIENT)
            t.modify_cs(MyTableTool.USE_TYPE_CLIENT)
        if use_type == MyTableTool.USE_TYPE_SERVER or use_type == MyTableTool.USE_TYPE_ALL:
            t.to_cs(MyTableTool.USE_TYPE_SERVER)
            t.modify_cs(MyTableTool.USE_TYPE_SERVER)
    
    Config.generate_proto_py_file('common_*')
    if use_type == MyTableTool.USE_TYPE_CLIENT or use_type == MyTableTool.USE_TYPE_ALL:
        Config.generate_proto_py_file('c_table_*')
    if use_type == MyTableTool.USE_TYPE_SERVER or use_type == MyTableTool.USE_TYPE_ALL:
        Config.generate_proto_py_file('s_table_*')

    os.chdir(work_path)
    
    for t in tables:
        if use_type == MyTableTool.USE_TYPE_CLIENT or use_type == MyTableTool.USE_TYPE_ALL:
            t.to_data(MyTableTool.USE_TYPE_CLIENT)
        if use_type == MyTableTool.USE_TYPE_SERVER or use_type == MyTableTool.USE_TYPE_ALL:
            t.to_data(MyTableTool.USE_TYPE_SERVER)

def RunAsync(use_type):
    for i in range(4):
        t = ThreadHandleTable(use_type, ThreadHandleTable.F_PROTO, que_table_path, que_table_path)
        t.setDaemon(True)
        t.start()
    
    FindTables(use_type, 1)
    CleanOutput(use_type)

    que_table_path.join()
    
    work_path = os.getcwd()
    os.chdir(config.proto_path)

    for i in range(4):
        t = ThreadHandleTable(use_type, ThreadHandleTable.F_CS, que_to_cs, que_to_cs)
        t.setDaemon(True)
        t.start()
    
    Config.generate_proto_py_file('common_*')
    if use_type == MyTableTool.USE_TYPE_CLIENT or use_type == MyTableTool.USE_TYPE_ALL:
        Config.generate_proto_py_file('c_table_*')
    if use_type == MyTableTool.USE_TYPE_SERVER or use_type == MyTableTool.USE_TYPE_ALL:
        Config.generate_proto_py_file('s_table_*')

    que_to_cs.join()
    os.chdir(work_path)

    for i in range(4):
        t = ThreadHandleTable(use_type, ThreadHandleTable.F_ALL, que_to_data, que_modify_cs)
        t.setDaemon(True)
        t.start()
    
    que_modify_cs.join()
    que_to_data.join()

if __name__ == '__main__':

    start_time = time.time()
    
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    success, args = ParseArg(sys.argv)
    if not success:
        Usage()
        exit(-1)

    use_type = MyTableTool.USE_TYPE_ALL

    logger.reset()
    logger.info('ready')

    CleanProto(use_type)

    #RunSync(use_type)
    RunAsync(use_type)

    logger.error('finish useTime:' + str(time.time() - start_time))
