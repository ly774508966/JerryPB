#!/usr/bin/python
# encoding=utf-8

import sys, os, Queue, threading, time, shutil
from logger import Logger
from config import Config

config = Config()
logger = Logger(Logger.LEVEL_INFO, 'table_tools')

que_py = Queue.Queue()
que_cs = Queue.Queue()

class TaskInfo():
    def __init__(self, val, opath):
        self.val = val
        self.opath = opath

def ParseArg(argv):
    if len(argv) < 1:
        return False, None
    return True, None

def Usage():
    print 'this is Usage()'
    print 'packCmd.py'
    
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

def CleanProto():
    DeleteFile(config.proto_path, config.common_prefix, '.py')
    DeleteFile(config.proto_path, config.common_prefix, '.pyc')
    DeleteFile(config.proto_path, config.command_prefix, '.py')
    DeleteFile(config.proto_path, config.command_prefix, '.pyc')

def CleanOutput():
    DeleteFile(config.common_cs_path, '.cs')
    DeleteFile(config.command_cs_path, '.cs')

def FindCommonAndCommand():
    list = os.listdir(config.proto_path)
    for filename in list:
        if filename.find('.proto') != -1 and (filename.startswith('common_') or filename.startswith('command_')):
            opath = config.command_cs_path
            if filename.startswith('common_'):
                opath = config.common_cs_path
            filenameWithoutExtension = os.path.splitext(filename)[0]    
            que_py.put(TaskInfo(filenameWithoutExtension, opath))

class ThreadHandleCommonAndCommand(threading.Thread):
    def __init__(self, que, flag):
        threading.Thread.__init__(self)
        self.que = que
        self.flag = flag
    def run(self):
        while True:
            if self.flag == 0:
                data = self.que.get()
                Config.generate_proto_py_file(data.val)
                que_cs.put(TaskInfo(data.val, data.opath))
                self.que.task_done()
            elif self.flag == 1:
                data = self.que.get()
                proto_name = '{}.proto'.format(data.val)
                cs_path = '{}{}.cs'.format(data.opath + '/', data.val)
                Config.proto_to_cs(proto_name, cs_path)
                Config.delete_xml(cs_path)
                self.que.task_done()

def RunAsync():
    work_path = os.getcwd()
    FindCommonAndCommand()
    
    thread_cnt = que_py.qsize() / 2
    if thread_cnt < 2:
        thread_cnt = 2;
    if thread_cnt > 20:
        thread_cnt = 20
        
    # gen py
    os.chdir(config.proto_path)
    for i in range(thread_cnt):
        t = ThreadHandleCommonAndCommand(que_py, 0)
        t.setDaemon(True)
        t.start()
        
    que_py.join()
    
    # gen cs
    os.chdir(config.proto_path)
    for i in range(thread_cnt):
        t = ThreadHandleCommonAndCommand(que_cs, 1)
        t.setDaemon(True)
        t.start()
        
    que_cs.join()
    os.chdir(work_path)

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
    CopyDir(config.command_cs_path, config.unity_command_cs_path, '.cs')

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
    
    CleanProto()
    CleanOutput()
    RunAsync()
    CopyClientFile()

    logger.error('finish useTime:' + str(time.time() - start_time))
