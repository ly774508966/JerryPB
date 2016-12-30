#!/usr/bin/python
# encoding=utf-8

import sys, os, Queue, threading, time, shutil
import xlrd
from logger import Logger
from myTable import MyTable, MyTableTool
from config import Config

config = Config()
logger = Logger(Logger.LEVEL_INFO, 'table_tools')

que_table_path = Queue.Queue()
que_to_data = Queue.Queue()
que_to_cs = Queue.Queue()
que_to_py = Queue.Queue()
que_modify_cs = Queue.Queue()
que_common_py = Queue.Queue()
que_common_cs = Queue.Queue()

class TaskInfo():
    def __init__(self, table, use_type):
        self.table = table
        self.use_type = use_type

def ParseArg(argv):
    use_type = MyTableTool.USE_TYPE_NONE
    do_copy = False
    par = ''
    
    if len(argv) < 1:
        return False, None
    elif len(argv) == 1:
        file_name = argv[0]
        file_name = os.path.split(file_name)[1]
        file_name = file_name.split('.')[0]

        file_names = file_name = file_name.split('_', 1)
        if len(file_names) != 2:
            return True, [use_type, do_copy]
        par = file_names[1]
    elif len(argv) == 2:
        par = argv[1]

    if par != '':
        pars = par.split('_')
        for p in pars:
            ps = p.split('-')
            if len(ps) == 2:
                if ps[0] == 'type':
                    if ps[1] == 'all':
                        use_type = MyTableTool.USE_TYPE_ALL
                    elif ps[1] == 'client':
                        use_type = MyTableTool.USE_TYPE_CLIENT
                    elif ps[1] == 'server':
                        use_type = MyTableTool.USE_TYPE_SERVER
                if ps[0] == 'copy':
                    if ps[1] == '0':
                        do_copy = False
                    elif ps[1] == '1':
                        do_copy = True
    
    return True, [use_type, do_copy]

def Usage():
    print 'this is Usage()'
    print 'run_type-client_copy-0.py'
    print 'run.py type-client_copy-0'

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
    DeleteFile(config.proto_path, config.common_prefix, '.py')
    DeleteFile(config.proto_path, config.common_prefix, '.pyc')
    if use_type == MyTableTool.USE_TYPE_ALL:
        DeleteFile(config.proto_path, '_table_', '.proto')
        # 下面两个文件不删除的话，表格文件命名大小写修改后，不会新创建解析文件
        DeleteFile(config.proto_path, '_table_', '.py')
        DeleteFile(config.proto_path, '_table_', '.pyc')
    elif use_type == MyTableTool.USE_TYPE_CLIENT:
        DeleteFile(config.proto_path, config.client_table_prefix, '.proto')
        DeleteFile(config.proto_path, config.client_table_prefix, '.py')
        DeleteFile(config.proto_path, config.client_table_prefix, '.pyc')
    elif use_type == MyTableTool.USE_TYPE_SERVER:
        DeleteFile(config.proto_path, config.server_table_prefix, '.proto')
        DeleteFile(config.proto_path, config.server_table_prefix, '.py')
        DeleteFile(config.proto_path, config.server_table_prefix, '.pyc')

def CleanOutput(use_type):
    DeleteFile(config.common_cs_path, '.cs')
    if use_type == MyTableTool.USE_TYPE_ALL:
        DeleteFile(config.table_cs_path, '.cs')
        DeleteFile(config.table_data_path, '.bytes')
    elif use_type == MyTableTool.USE_TYPE_CLIENT:
        DeleteFile(config.table_cs_path, '.cs', config.client_table_prefix)
        DeleteFile(config.table_data_path, '.bytes', config.client_table_prefix)
    elif use_type == MyTableTool.USE_TYPE_SERVER:
        DeleteFile(config.table_cs_path, '.cs', config.server_table_prefix)
        DeleteFile(config.table_data_path, '.bytes', config.server_table_prefix)

def FindCommon():
    list = os.listdir(config.proto_path)
    for filename in list:
        if filename.find('.proto') != -1 and filename.startswith('common_'):
            filenameWithoutExtension = os.path.splitext(filename)[0]
            que_common_py.put(filenameWithoutExtension)

def FindTables(use_type):
    list = os.listdir(config.table_path)
    for filename in list:
        if filename.find('.xlsx') != -1:
            que_table_path.put(config.table_path + '\\' + filename)

class ThreadHandleCommon(threading.Thread):
    def __init__(self, que, flag):
        threading.Thread.__init__(self)
        self.que = que
        self.flag = flag
    def run(self):
        while True:
            if self.flag == 0:
                data = self.que.get()
                Config.generate_proto_py_file(data)
                que_common_cs.put(data)
                self.que.task_done()
            elif self.flag == 1:
                data = self.que.get()
                proto_name = '{}.proto'.format(data)
                cs_path = '{}{}.cs'.format(config.common_cs_path + '/', data)
                Config.proto_to_cs(proto_name, cs_path)
                Config.delete_xml(cs_path)
                self.que.task_done()

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
                    que_to_py.put(TaskInfo(table, MyTableTool.USE_TYPE_CLIENT))
		    que_to_cs.put(TaskInfo(table, MyTableTool.USE_TYPE_CLIENT))
                    que_modify_cs.put(TaskInfo(table, MyTableTool.USE_TYPE_CLIENT))
                if self.use_type == MyTableTool.USE_TYPE_SERVER or self.use_type == MyTableTool.USE_TYPE_ALL:
                    que_to_py.put(TaskInfo(table, MyTableTool.USE_TYPE_SERVER))
		    que_to_cs.put(TaskInfo(table, MyTableTool.USE_TYPE_SERVER))
                    que_modify_cs.put(TaskInfo(table, MyTableTool.USE_TYPE_SERVER))

                if self.use_type == MyTableTool.USE_TYPE_CLIENT or self.use_type == MyTableTool.USE_TYPE_ALL:
                    que_to_data.put(TaskInfo(table, MyTableTool.USE_TYPE_CLIENT))
                if self.use_type == MyTableTool.USE_TYPE_SERVER or self.use_type == MyTableTool.USE_TYPE_ALL:
                    que_to_data.put(TaskInfo(table, MyTableTool.USE_TYPE_SERVER))
                    
                self.que.task_done()
            elif self.flag == self.F_CS:
		if self.que.empty() == False:
		    data = self.que.get()
		    data.table.to_cs(data.use_type)
		    self.que.task_done()
		else:
		    data = self.que2.get()
		    table_prefix = ''
		    if data.use_type == MyTableTool.USE_TYPE_CLIENT:
                        table_prefix = config.client_table_prefix
		    else:
                        table_prefix = config.server_table_prefix
		    Config.generate_proto_py_file('{}{}'.format(table_prefix, data.table.name))
		    self.que2.task_done()
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

def RunAsync(use_type):
    work_path = os.getcwd()
    
    FindCommon()
    
    thread_cnt2 = que_common_py.qsize() / 2
    if thread_cnt2 < 2:
        thread_cnt2 = 2;
    if thread_cnt2 > 20:
        thread_cnt2 = 20

    thread_cnt = que_table_path.qsize() / 3
    if thread_cnt < 2:
        thread_cnt = 2;
    if thread_cnt > 20:
        thread_cnt = 20

    # gen common py
    os.chdir(config.proto_path)
    for i in range(thread_cnt2):
        t = ThreadHandleCommon(que_common_py, 0)
        t.setDaemon(True)
        t.start()
        
    FindTables(use_type)
    que_common_py.join()

    # gen table proto
    os.chdir(work_path)
    for i in range(thread_cnt):
        t = ThreadHandleTable(use_type, ThreadHandleTable.F_PROTO, que_table_path, que_table_path)
        t.setDaemon(True)
        t.start()
    que_table_path.join()

    # gen cs, gen table py
    os.chdir(config.proto_path)
    for i in range(thread_cnt2):
        t = ThreadHandleCommon(que_common_cs, 1)
        t.setDaemon(True)
        t.start()
        
    for i in range(thread_cnt):
        t = ThreadHandleTable(use_type, ThreadHandleTable.F_CS, que_to_cs, que_to_py)
        t.setDaemon(True)
        t.start()

    que_common_cs.join()
    que_to_cs.join()
    que_to_py.join()

    # modify table cs, gen table data
    os.chdir(work_path)
    for i in range(thread_cnt):
        t = ThreadHandleTable(use_type, ThreadHandleTable.F_ALL, que_to_data, que_modify_cs)
        t.setDaemon(True)
        t.start()
    
    que_modify_cs.join()
    que_to_data.join()

def CleanDir(dir_path, pattern = ''):
    if os.path.exists(dir_path) == False:
        return
    
    list = os.listdir(dir_path)
    for filename in list:
        if pattern == '' or filename.find(pattern) != -1:
            os.remove(dir_path + '/' + filename)

def CopyDir(s, t, pattern = ''):
    if os.path.exists(s) == False:
        return
    
    if os.path.exists(t) == False:
        os.mkdir(dir_path)

    list = os.listdir(s)
    for filename in list:
        if pattern != '' and filename.find(pattern) == -1:
            continue
        # Unity中，不做删除的话，同名文件，只是大小写不一样，文件名不会替换
        if os.path.exists('{}/{}'.format(t, filename)):
            os.remove('{}/{}'.format(t, filename))
        shutil.copy('{}/{}'.format(s, filename), '{}/{}'.format(t, filename))

def CopyClientFile():
    CopyDir(config.common_cs_path, config.unity_common_cs_path, '.cs')
    CopyDir(config.table_cs_path, config.unity_table_cs_path, config.client_table_prefix)
    CopyDir(config.table_data_path, config.unity_table_data_path, config.client_table_prefix)

if __name__ == '__main__':
    start_time = time.time()
    ttt = start_time
    reload(sys)
    sys.setdefaultencoding('utf-8')

    success, args = ParseArg(sys.argv)
    if not success:
        Usage()
        exit(-1)

    logger.reset()

    use_type = args[0]
    do_copy = args[1]

    str_use_type = 'None'
    if use_type == MyTableTool.USE_TYPE_CLIENT:
        str_use_type = 'Client'
    elif use_type == MyTableTool.USE_TYPE_ALL:
        str_use_type = 'All'
    elif use_type == MyTableTool.USE_TYPE_SERVER:
        str_use_type = 'Server'
    elif use_type == MyTableTool.USE_TYPE_NONE:
        str_use_type = 'None'
    logger.info('ready type=' + str_use_type)

    if use_type != MyTableTool.USE_TYPE_NONE:
        CleanProto(use_type)
        CleanOutput(use_type)
        RunAsync(use_type)
    if do_copy == True:
        CopyClientFile()

    logger.error('finish useTime:' + str(time.time() - start_time))
