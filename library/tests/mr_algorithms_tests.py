'''
Created on Jul 13, 2011

@author: kykamath
'''
import sys
from StringIO import StringIO
sys.path.append('../')
import unittest
from mr_algorithms import WordCountSample1, WordCountSample2

class MRJobWrapperTests(unittest.TestCase):
    def setUp(self):
        self.testString='Sachin Tendulkar is one century away from reaching 100 international'
        self.log1 = '../data/log1'
        self.wcSample1 = WordCountSample1()
        self.wcSample2 = WordCountSample2()
    def test_mapper(self): self.assertEqual([(w,1)for w in self.testString.split()], list(self.wcSample1.mapper('', self.testString)))
    def test_reducer(self): self.assertEqual([('foo', 2)], list(self.wcSample1.reducer('foo', [1, 1])))
    def test_makeRunner(self):
        sys.stdin = StringIO(self.testString)
        mr_job = WordCountSample1(args=[])
        with mr_job.make_runner() as runner:
            runner.run()
            self.assertEqual([(w,1)for w in sorted(self.testString.split())], [mr_job.parse_output_line(line) for line in runner.stream_output()])
    def test_runJob(self): 
        self.assertEqual([(w,1)for w in sorted(self.testString.split())], list(self.wcSample1.runJob(inputFileList=[self.log1])))
        self.assertEqual([(w,1)for w in sorted(self.testString.split())], list(self.wcSample2.runJob(inputFileList=[self.log1])))

if __name__ == '__main__':
    unittest.main()
#    sys.stdin = file('../data/log_data')
#    mr_job = WordCountSample1(args=[])
#    print mr_job.job_runner_kwargs()
#    mr_job.args = ['../data/log1', '../data/log2']
##    mr_job.add_file_option('--file', '../data/log1')
#    print mr_job.job_runner_kwargs()
#    with mr_job.make_runner() as runner:
#        runner.run()
#        print [mr_job.parse_output_line(line) for line in runner.stream_output()]
