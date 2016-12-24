#!/usr/bin/python
# encoding=utf-8

import sys, os

def Usage():
    print 'this is Usage()'
    print 'run_type-client_copy-0.py'
    
def ParseArg(argv):

    if len(argv) < 1:
        return False, None
    elif len(argv) == 1:
        file_name = argv[0]
        file_name = os.path.split(file_name)[1]
        file_name = file_name.split('.')[0]
        file_names = file_name = file_name.split('_', 1)
        if len(file_names) != 2:
            return False, None
        par = file_names[1]
        return True, [par]
    return False, None

def execute_shell_command(args, wait = 'T'):
    p = subprocess.Popen(args)
    if wait == 'T':
	ret = p.wait()
	return ret
    else:
	return 0

if __name__ == '__main__':
    
    reload(sys)
    sys.setdefaultencoding('utf-8')

    success, args = ParseArg(sys.argv)
    if not success:
        Usage()
        exit(-1)

    os.system('run.py ' + args[0])

    

    
