'''
Created on Jul 14, 2011

@author: kykamath
'''
from mrjob.job import MRJob
class UsingOptionsMRJob(MRJob):
    def configure_options(self):
        super(UsingOptionsMRJob, self).configure_options()
        self.add_passthrough_option( '--val1', dest='val1', default=':ilab:', help='provide a val1')
    def load_options(self, args):
        """Parse stop_words option."""
        super(UsingOptionsMRJob, self).load_options(args)
        self.val1 = self.options.val1
    def mapper(self, key, value):
        for word in value.split():
            yield word+self.val1, 1
    def reducer(self, key, values): 
        yield key, sum(values)
    
if __name__ == '__main__':
    UsingOptionsMRJob.run()