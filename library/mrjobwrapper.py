'''
Created on Jul 14, 2011

@author: kykamath

A wrapper for mrjob module. This defines some methods and classes
that I will be using regularly.
'''
import sys, cjson
from mrjob.conf import dump_mrjob_conf, combine_dicts
from mrjob.protocol import HadoopStreamingProtocol
from mrjob.job import MRJob

class MRJobWrapper():
    ''' MARKED FOR REMOVAL. DO NOT USE THIS.
    '''
    def _setOptions(self, **kwargs):
        self.mrjob.args = kwargs.get('inputFileList', self.mrjob.args)
        self.mrjob.options.jobconf = combine_dicts(self.mrjob.options.jobconf, kwargs.get('jobconf', self.mrjob.options.jobconf))
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


class WritableObject:
    def __init__(self):
        self.content = []
    def write(self, string):
        self.content.append(string)

def  updateMRJobConf():
    conf = {'runners':{
                'hadoop':{'python_archives': ['/home/kykamath/projects/library/dist/my_library-1.0.tar.gz']}
                }
            }
    with open('/Users/kykamath/.mrjob', 'w') as f: dump_mrjob_conf(conf, f)
   
class CJSONProtocol(HadoopStreamingProtocol):
    """A cjson wrapper for CJSONProtocol.
    """
    ID = 'cjson'
    @classmethod
    def read(cls, line):
        key, value = line.split('\t')
        return cjson.decode(key), cjson.decode(value)
    @classmethod
    def write(cls, key, value): return '%s\t%s' % (cjson.encode(key), cjson.encode(value))
    
class ModifiedMRJob(MRJob):
    DEFAULT_INPUT_PROTOCOL=CJSONProtocol.ID
    DEFAULT_PROTOCOL=CJSONProtocol.ID
    def _setOptions(self, **kwargs):
        self.args = kwargs.get('inputFileList', self.args)
        self.options.jobconf = combine_dicts(self.options.jobconf, kwargs.get('jobconf', self.options.jobconf))
    def emptyMapper(self, key, line): yield key, line
    def runJob(self, **kwargs):
        self._setOptions(**kwargs)
        with self.make_runner() as runner:
            runner.run()
            for line in runner.stream_output(): yield self.parse_output_line(line)
    def runMapper(self, **kwargs):
        self._setOptions(**kwargs)
        reader = self.protocols()[self.DEFAULT_OUTPUT_PROTOCOL or self.DEFAULT_PROTOCOL]
        mapperOutput = WritableObject()
        self.stdout = mapperOutput
        self.run_mapper()
        sys.stdout = sys.__stdout__ 
        for i in filter (lambda a: a != '\n', mapperOutput.content): yield reader.read(i)
    
    ''' Jobs to count number of keys.
    '''
    def mapper_count_key(self, key, _): yield 1, key
    def reducer_count_key(self, _, values): yield 1, {'total': len(list(values))}
    def jobsToCountNumberOfKeys(self): return [self.mr(mapper=self.mapper_count_key, reducer=self.reducer_count_key)]
            
    @classmethod
    def protocols(cls):
        protocol_dict = super(ModifiedMRJob, cls).protocols()
        protocol_dict[CJSONProtocol.ID] = CJSONProtocol
        return protocol_dict
    
