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
from file_io import FileIO
from classes import GeneralMethods

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
   
#class CJSONProtocol(HadoopStreamingProtocol):
#    """A cjson wrapper for CJSONProtocol.
#    """
#    ID = 'cjson'
#    @classmethod
#    def read(cls, line):
#        key, value = line.split('\t')
#        return cjson.decode(key), cjson.decode(value)
#    @classmethod
#    def write(cls, key, value): return '%s\t%s' % (cjson.encode(key), cjson.encode(value))

class CJSONProtocol(HadoopStreamingProtocol):
    """A cjson wrapper for CJSONProtocol.
    """
    ID = 'cjson'
    @classmethod
    def read(cls, line):
        splits = line.split('\t')
        if len(splits)==2: key, value = splits
        else: key, value = 'null', splits[0]
        return cjson.decode(key), cjson.decode(value)
    @classmethod
    def write(cls, key, value): return '%s\t%s' % (cjson.encode(key), cjson.encode(value))

def runMRJob(mrJobClass,
             outputFileName,
             inputFileList,
             mrJobClassParams = {},
             args='-r hadoop'.split(),
             **kwargs):
    mrJob = mrJobClass(args=args, **mrJobClassParams)
    GeneralMethods.runCommand('rm -rf %s'%outputFileName)
    for l in mrJob.runJob(inputFileList=inputFileList, **kwargs): FileIO.writeToFileAsJson(l[1], outputFileName)

def runMRJobAndYieldResult(mrJobClass,
                           inputFileList,
                           mrJobClassParams = {},
                           args='-r hadoop'.split(),
                           **kwargs):
    mrJob = mrJobClass(args=args, **mrJobClassParams)
    for l in mrJob.runJob(inputFileList=inputFileList, **kwargs): yield l[1]

class ModifiedMRJob(MRJob):
    DEFAULT_INPUT_PROTOCOL=CJSONProtocol.ID
    DEFAULT_PROTOCOL=CJSONProtocol.ID
    def __init__(self, args=None, **kwargs):
        super(ModifiedMRJob, self).__init__(args=args)
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
    
    ''' Start: Jobs to count number of keys.
    '''
    def mapper_count_key(self, key, _): yield 1, key
    def reducer_count_key(self, _, values): yield 1, {'total': len(list(values))}
    def jobsToCountNumberOfKeys(self): return [self.mr(mapper=self.mapper_count_key, reducer=self.reducer_count_key)]
    ''' End: Jobs to count number of keys.
    '''
#    
#    ''' Start: Jobs to find stable Markov modelling process.
#        Got this code from: https://github.com/Yelp/mrjob/blob/development/mrjob/examples/mr_page_rank.py
#    '''
#    def send_score(self, node_id, node):
#        """Mapper: send score from a single node to other nodes.
#
#        Input: ``node_id, node``
#
#        Output:
#        ``node_id, ('node', node)`` OR
#        ``node_id, ('score', score)``
#        """
#        yield node_id, ('node', node)
#        for dest_id, weight in node.get('links') or []: yield dest_id, ('score', node['score'] * weight)
#    def receive_score(self, node_id, typed_values):
#        """Reducer: Combine scores sent from other nodes, and update this node
#        (creating it if necessary).
#
#        Store information about the node's previous score in *prev_score*.
#        """
#        node = {}
#        total_score = 0
#        for value_type, value in typed_values:
#            if value_type == 'node': node = value
#            else:
#                assert value_type == 'score'
#                total_score += value
#        node['prev_score'] = node['score']
#        d = self.options.damping_factor
#        node['score'] = 1 - d + d * total_score
#        yield node_id, node
#    def getJobsToGetStableTransitionProbabilities(self): return ([self.mr(mapper=self.send_score, reducer=self.receive_score)] * self.options.iterations)
#    ''' End: Jobs to find stable Markov modelling process.
#    '''
    
            
    @classmethod
    def protocols(cls):
        protocol_dict = super(ModifiedMRJob, cls).protocols()
        protocol_dict[CJSONProtocol.ID] = CJSONProtocol
        return protocol_dict
    
