'''
Created on Jun 23, 2011

@author: kykamath
'''
import unittest, sys
sys.path.append('../')
from classes import GeneralMethods
from pig import Pig

class FileIOTests(unittest.TestCase):
    def setUp(self):
        self.f1 = 'f1'
        self.f2 = 'f2'
        open(self.f1, 'w').write('a\nb\n')
        open(self.f2, 'w').write('1\n2\n')
    def test_combine_files(self):
        pig = Pig([self.f1, self.f2], [])
        pig.run()
        GeneralMethods.runCommand('cat %s'%pig.output_pig_script)
    def tearDown(self):
        GeneralMethods.remove_file(self.f1)
        GeneralMethods.remove_file(self.f2)
        GeneralMethods.remove_file('pig_tests.pig')
        
if __name__ == '__main__':
    unittest.main()