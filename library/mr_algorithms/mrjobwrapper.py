'''
Created on Jul 14, 2011

@author: kykamath
'''
from mrjob.job import MRJob
class MRJobWrapper(MRJob):
    '''
    A wrapper for MRJob. This defines some methods that I
    will be using regularly.
    '''
    def __init__(self, *args, **kwargs): super(MRJobWrapper, self).__init__(*args, **kwargs)
    def runJob(self, inputFileList):
        self.args = inputFileList
        with self.make_runner() as runner:
            runner.run()
            for line in runner.stream_output(): yield self.parse_output_line(line)
