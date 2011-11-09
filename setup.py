'''
Created on Jul 10, 2011

@author: kykamath
'''
from distutils.core import setup
setup(name='my_library',
      version='1.0',
      description='A collection of modules used by different projects.',
      author='Krishna Y. Kamath',
      author_email='krishna.kamath@gmail.com',
      url='https://github.com/kykamath/library',
      packages=['library', 'library.mr_algorithms', 'library.graphs', 'library.weka'],
#      data_files=[('lib/python2.6/site-packages/library/data', ['library/data/stop_words.json'])]
      )

