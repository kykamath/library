'''
Created on Jul 14, 2011

@author: kykamath
'''
from mrjob.job import MRJob
from mrjobwrapper import CJSONProtocol

class WordCountMRJob(MRJob):
    DEFAULT_INPUT_PROTOCOL=CJSONProtocol.ID
    DEFAULT_PROTOCOL=CJSONProtocol.ID
    def mapper(self, key, value):
        for word in value.split(): yield word, 1
    def reducer(self, key, values): yield key, sum(values)
    @classmethod
    def protocols(cls):
        protocol_dict = super(WordCountMRJob, cls).protocols()
        protocol_dict[CJSONProtocol.ID] = CJSONProtocol
        return protocol_dict
    
if __name__ == '__main__':
    #Give the next line as input. 
    #"doc_id_1"    "Sachin Tendulkar is one century away from reaching 100 international"
    WordCountMRJob.run()