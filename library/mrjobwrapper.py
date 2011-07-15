'''
Created on Jul 14, 2011

@author: kykamath
'''
import sys
from mrjob.job import MRJob

class WritableObject:
    def __init__(self):
        self.content = []
    def write(self, string):
        self.content.append(string)

class MRJobWrapper(MRJob):
    '''
    A wrapper for MRJob. This defines some methods that I
    will be using regularly.
    '''
    def __init__(self, *args, **kwargs): super(MRJobWrapper, self).__init__(*args, **kwargs)
    def _setOptions(self):
        self.options.python_archives = ['/'.join(__file__.split('/')[:-2])+'/dist/my_library-1.0.tar.gz']
    def runJob(self, inputFileList):
        self._setOptions()
        self.args = inputFileList
        with self.make_runner() as runner:
            runner.run()
            for line in runner.stream_output(): yield self.parse_output_line(line)
    def runMapper(self, inputFileList):
        self._setOptions()
        self.args = inputFileList
        reader = self.protocols()[self.DEFAULT_OUTPUT_PROTOCOL or self.DEFAULT_PROTOCOL]
        mapperOutput = WritableObject()
        self.stdout = mapperOutput
        self.run_mapper()
        sys.stdout = sys.__stdout__ 
        for i in filter (lambda a: a != '\n', mapperOutput.content): yield reader.read(i)
