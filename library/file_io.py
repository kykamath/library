'''
Created on Jun 13, 2011

@author: kykamath
'''
from classes import GeneralMethods
from itertools import imap
import cjson
import os
import random
import string

class FileIO:
    @staticmethod
    def createDirectoryForFile(path):
        dir = path[:path.rfind('/')]
        if not os.path.exists(dir): os.umask(0), os.makedirs('%s'%dir, 0777)
    @staticmethod
    def writeToFileAsJson(data, file):
        FileIO.createDirectoryForFile(file)
        f = open('%s'%file, 'a')
        f.write(cjson.encode(data)+'\n')
        f.close()
    @staticmethod
    def writeToFile(data, file):
        FileIO.createDirectoryForFile(file)
        f = open('%s'%file, 'a')
        f.write(data+'\n')
        f.close()
    @staticmethod
    def iterateJsonFromFile(file, remove_params_dict=False):
        for line in open(file): 
            try:
                if not remove_params_dict: yield cjson.decode(line)
                else:
                    data = cjson.decode(line)
                    if 'PARAMS_DICT' not in data: yield data
            except: pass
    @staticmethod
    def getFileByDay(currentTime):
        return '_'.join([str(currentTime.year), str(currentTime.month), str(currentTime.day)])
    @staticmethod
    def iterateLinesFromFile(filePath, commentCharacter='#'):
        for line in open(filePath):
            if not line.startswith(commentCharacter): yield line.strip()
    @staticmethod
    def iter_json_from_hdfs_output(f):
        return imap(lambda d: cjson.decode(d.strip().split('\t')[1]), file(f))
    @staticmethod
    def write_file_from_hdfs_to_local_file(hdfs_file, f_local):
        f_temp_output = '/tmp/%s'%(''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10)))
        GeneralMethods.runCommand('hadoop fs -cat %s/part* > %s'%(hdfs_file, f_temp_output))
        GeneralMethods.runCommand('rm -rf %s'%f_local)
        for data in file(f_temp_output): FileIO.writeToFile(data.strip().split('\t')[1], f_local)
        GeneralMethods.runCommand('rm -rf %s'%f_temp_output)
            