'''
Created on Jul 14, 2011

@author: kykamath
'''
import sys
from mrjob.conf import dump_mrjob_conf, combine_dicts

class WritableObject:
    def __init__(self):
        self.content = []
    def write(self, string):
        self.content.append(string)

class MRJobWrapper():
    '''
    A wrapper for MRJob. This defines some methods that I
    will be using regularly.
    '''
    def _setOptions(self, **kwargs):
        self.mrjob.args = kwargs.get('inputFileList', self.mrjob.args)
        print self.mrjob.options.jobconf
        self.mrjob.options.jobconf = combine_dicts(self.mrjob.options.jobconf, kwargs.get('jobconf', self.mrjob.options.jobconf))
        print self.mrjob.options.jobconf
    def runJob(self, **kwargs):
        self._setOptions(**kwargs)
        with self.mrjob.make_runner() as runner:
            runner.run()
            for line in runner.stream_output(): yield self.mrjob.parse_output_line(line)
    def runMapper(self, **kwargs):
        self._setOptions(**kwargs)
        reader = self.mrjob.protocols()[self.mrjob.DEFAULT_OUTPUT_PROTOCOL or self.mrjob.DEFAULT_PROTOCOL]
        mapperOutput = WritableObject()
        self.mrjob.stdout = mapperOutput
        self.mrjob.run_mapper()
        sys.stdout = sys.__stdout__ 
        for i in filter (lambda a: a != '\n', mapperOutput.content): yield reader.read(i)
    def mapper(self, key, value): return self.mrjob.mapper(key, value)
    def reducer(self, key, values): return self.mrjob.reducer(key, values)
        
def  updateMRJobConf():
    conf = {'runners':{
                'hadoop':{'python_archives': ['/home/kykamath/projects/library/dist/my_library-1.0.tar.gz']}
                }
            }
    with open('/Users/kykamath/.mrjob', 'w') as f: dump_mrjob_conf(conf, f)
