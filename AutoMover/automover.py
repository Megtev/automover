"""
To work full value with this module you have to use
init_log_file(log file name) to initialize log_file,
but now it doesn't work properly as module
"""

import os, shutil, time, sys, copy

class File:                                         # Class for comfort using files
    """
    File(path, name)
    where path is a full path for file, and name it's a name of file
    """
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def __repr__(self):
        return self.name

    def __oldert(self, file):                       # return True if 'file' older
        """
        Checkin who is older, this file,
        or file in bracket
        """
        return os.path.getmtime(self.path) > os.path.getmtime(file.path)

    def selfcopy(self, file):
        """
        Trying to copy itself to any place
        and write down result into log file (it's in 'AutoMover/Log/' folder)
        """
        try:
            shutil.copy2(self.path, file.path)
            log_file.write("{0}-{1}-{2}.{3}:{4}:{5}:  Copying '{6}' to '{7}'\n".format(
                            *time.strftime('%D/%H/%M/%S').split('/'), self.path, file.path))
        except PermissionError:
            log_file.write("{0}-{1}-{2}.{3}:{4}:{5}:  PermissionError: can't copy '{6}' to '{7}'\n".format(
                            *time.strftime('%D/%H/%M/%S').split('/'), self.path, file.path))
        finally:
            log_file.flush()

    def substitution(self, folder):
        """
        It will exchanche itself to file with the same name in current folder,
        if the file is older
        """
        for x in range(len(folder)):
            if type(folder[x]) == type([]):
                self.substitution(folder[x])
            elif self.name == folder[x].name and self.path != folder[x].path and self.__oldert(folder[x]):
                self.selfcopy(folder[x])

log_file = None

def init_log_file(file_log_name):                   # Initialize log_file
    global log_file
    log_file = open(file_log_name, mode='w', encoding='utf-8')

def exception_list(x, exc_list):                    # Return True if the file in file_exceptionList.txt
    if x in exc_list: return True
    if x.startswith('~$') or x.endswith('.tmp'): return True

def nfiles(path):                                   # Moving every folders and files into list with instance of class File
    temp_files = os.listdir(path)
    lfiles = []
    exception_file = open(os.path.abspath(os.path.dirname(sys.argv[0])) + '\\file_exceptionList.txt', mode='r')
    exc_list = (x.rstrip() for x in exception_file.readlines() if not x.startswith('#'))
    exception_file.close()
    
    for x in temp_files:
        if os.path.isfile(path + '\\' + x):
            if not exception_list(x, exc_list):
                new_folder[path + '\\' + x] = os.path.getmtime(path + '//' + x)
                lfiles.append(File(path + '\\' + x, x))
        else:
            lfiles.append(nfiles(path + '\\' + x))
    return lfiles

def selfchecker(folder, main_folder=None):          # Checking itself if every file have been changed
    if main_folder == None: main_folder = folder[:]
    for x in range(len(folder)):
        if isinstance(folder[x], File) and updated(folder[x]): # Checking itself with everyfile in a main_folder
            folder[x].substitution(main_folder)
        elif type(folder[x]) == type([]):
            selfchecker(folder[x], main_folder)

def updated(file):                                  # Checking itself: returns True if last
    try:                                            # version of a file older than current version
        if os.path.getmtime(file.path) > last_folder[file.path]: return True
    except KeyError:
        return True

if __name__ == '__main__':
    temp_file = open(os.path.abspath(os.path.dirname(sys.argv[0])) + '\\start.txt').read().rstrip()
    if temp_file != '':
        strfolder = temp_file
    else:
        try:
            strfolder = sys.argv[1]                     # Can work a little bit with command line
        except IndexError:
            strfolder = input("Please write down a path of folder: ")
    counter = 1
    last_folder = {}
    init_log_file('{0}\\Log\\{1}-{2}-{3}.{4}-{5}-{6}.log'.format(
                            os.path.abspath(os.path.dirname(sys.argv[0])),
                            *time.strftime('%D/%H/%M/%S').split('/')))

    while True:                                     # Endless cycle was made just for
        print(1)
        new_folder = {}
        main_folder = nfiles(strfolder)
        #print("\n\n------Attempt number " + str(counter) + '------')
        #print("starting selfchecking...")
        selfchecker(main_folder)
        #print("finished selfchecking...")
        time.sleep(10)
        counter += 1
        last_folder = copy.deepcopy(new_folder)