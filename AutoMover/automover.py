import os, shutil, time

class File:                         #Класс для удобного хранения даных про файл
    def __init__(self, path, name, typef):
        self.path = path
        self.name = name
        self.type = typef
    def __repr__(self):
        return self.name
    def __oldert(self, file):
        return os.path.getmtime(self.path) > os.path.getmtime(file.path)
    def selfcopy(self, file):
        print('copying %s to %s...' % (self.path, file.path))
        shutil.copy2(self.path, file.path)

    def substitution(self, folder):
        """?
        Заменяет себя на файл с одинаковым именем в заданой папке,
        если даный файл старше
        """
        #print(folder)
        for x in range(len(folder)):
            #print(folder[x])
            if type(folder[x]) == type([]):
                #print(folder[x])
                self.substitution(folder[x])
            elif self.name == folder[x].name and self.path != folder[x].path and self.__oldert(folder[x]):
                #print(folder[x])
                self.selfcopy(folder[x])

exlusion_list = ['Thumbs.db', 'Begin.pptx']

def exclusion(x):                   #Возвращает True если файл находится в исключениях
    if x in exlusion_list: return True
    if x.startswith('~$'): return True

def nfiles(path):                   #Переносит все папки и файлы в представление многоуровневых списков с экземплярами класса File
    temp_files = os.listdir(path)
    lfiles = []
    for x in temp_files:
        if os.path.isfile(path + '\\' + x):
            if not exclusion(x):
                lfiles.append(File(path + '\\' + x, x, 'file'))
        else:
            lfiles.append(nfiles(path + '\\' + x))
    return lfiles

def selfchecker(main_folder, folder):
    #print('selfch...', folder)
    for x in range(len(folder)):
        if type(folder[x]) != type([]):
            folder[x].substitution(main_folder)
        else:
            selfchecker(main_folder, folder[x])


if __name__ == '__main__':
    import sys
    try:
        strfolder = sys.argv[1]
    except IndexError:
        strfolder = input("Please write down a path of folder: ")
    counter = 1
    while True:
        main_folder = nfiles(strfolder)
        print("\n\n------Attempt number " + str(counter) + '------')
        print("starting selfchecking...")
        selfchecker(main_folder, main_folder)
        print("finished selfchecking...")
        time.sleep(15)
        counter += 1