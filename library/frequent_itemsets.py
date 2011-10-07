#!/usr/bin/python
#
# Python implementation of the Eclat frequent itemset mining algorithm.
# See "New algorithms for fast discovery of association rules" by Zaki et al.
# for details.
# Implementation by Michael Mampaey,  version 0.1.20091008.
#

import sys, os
from optparse import OptionParser
from classes import TwoWayMap, GeneralMethods

author  = "Michael Mampaey"
version = "%prog v0.1.20091008 "
#usage   = "Usage: %prog FILENAME MINSUP [options]"

# Input parsing
#parser = OptionParser(usage=usage, version=version)
#parser.add_option("-p", "--print", action="store_true", dest="output", default=False, help="print itemsets to stdout")
#parser.add_option("-o", "--output", action="store", dest="outfile", help="save itemsets to file", metavar="FILE")
#parser.add_option("", "--max-size", action="store", type="int", dest="maxsize", default=0, help="maximum itemset size")
#parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="verbose mode")
#
#(options, args) = parser.parse_args()
#if len(args) < 2:
#    sys.stderr.write("Usage: " + sys.argv[0] + " FILENAME MINSUP [options]" + '\n')
#    sys.exit(1)
#
#filename = args[0]
#minsup   = int(args[1])

#class Flusher:
#    """For flushing stdout
#    """
#    def __str__(self):
#        sys.stdout.flush()
#        return '\b'
#
#flush = Flusher()



class Itemset:
    """Itemset Class
    """
    def __init__(self, suffix=0):
        self.suffix = suffix
        self.support = 0
        self.tids = set()
    
    def __cmp__(self, other):
        return cmp(self.support, other.support)



class FIByEclat:
    """Eclat Class
    Modified the implementation of this algorithm by Michael Mampaey (http://adrem.ua.ac.be/michael.mampaey/implementations)
    """
    def __init__(self, transactionIterator, minsup, maxdepth=0):
#    def __init__(self, filename, minsup, output=False, outfilename=None, maxdepth=0, verbose=False):
#        self.filename    = filename
        self.transactionIterator = transactionIterator
        self.minsup      = minsup
        self.item_count  = 0
        self.trans_count = 0
#        self.output      = output
#        self.outfilename = outfilename
        self.maxdepth    = maxdepth
#        self.verbose     = verbose
        self.data        = None
#        return
        self.frequentItemsets = []
        self.itemToItemIdMap = {}
    
#    def read_data(self):
#        """Read data and return list of itemsets, in vertical format
#        """
#        self.item_count  = 0
#        self.trans_count = 0
#        self.data = []
#        self.data.append(Itemset(0))
#        
#        f = open(self.filename, 'r')
#        for row in f:
#            self.trans_count += 1
#            for item in map(int, row.split()):
#                if item > self.item_count:
#                    for i in range(self.item_count+1, item+1):
#                        self.data.append(Itemset(i))
#                    self.item_count = item
#                self.data[item].tids.add(self.trans_count)
#        f.close()
#        
#        for itemset in self.data:
#            itemset.support = len(itemset.tids)
#        return

    def read_data(self):
        """Read data and return list of itemsets, in vertical format
        """
        self.item_count  = 0
        self.trans_count = 0
        self.data = []
        self.data.append(Itemset(0))
        
#        f = open(self.filename, 'r')
        for itemset in self.transactionIterator:
            self.trans_count += 1
            for item in itemset:
                if item not in self.itemToItemIdMap: self.itemToItemIdMap[item]=len(self.itemToItemIdMap)+1
                item = self.itemToItemIdMap[item]
                if item > self.item_count:
                    for i in range(self.item_count+1, item+1): self.data.append(Itemset(i))
                    self.item_count = item
                self.data[item].tids.add(self.trans_count)
#        f.close()
        for itemset in self.data: itemset.support = len(itemset.tids)
        return
    
    def prune_items(self):
        """Prune the non-frequent items from the data
        """
        for i in range(len(self.data)-1, -1, -1):
            if self.data[i].support < self.minsup: del self.data[i]
        self.data.sort()
        return
    
    def eclat_mine(self, data=[], prefix=[], closure=[], clen = 0, depth=0):
        """Mines vertical data depth-first, rightmost for frequent itemsets
        """
        if self.maxdepth and depth+clen >= self.maxdepth: return 0
        
        counter = 0
        if depth == 0: counter = 1
#            if self.output: self.printset([], self.trans_count)
#            if self.outfilename: 
#            print self.trans_count
#            self.out.write('(' + str(self.trans_count) + ')' + '\n' )
        
        for i in range(len(data)):
            set1 = data[i]
            prefix.append(set1.suffix)
            children = []
            cl = clen
            
            for j in range(i+1, len(data)):
                set2 = data[j]
                tmpset = Itemset()
                tmpset.suffix = set2.suffix
                if depth < 1:
                    tmpset.tids = set1.tids & set2.tids
                    tmpset.support = len(tmpset.tids)
                elif depth == 1:
                    tmpset.tids = set1.tids - set2.tids
                    tmpset.support = set1.support - len(tmpset.tids)
                else:
                    tmpset.tids = set2.tids - set1.tids
                    tmpset.support = set1.support - len(tmpset.tids)
                if tmpset.support >= self.minsup:
                    if set1.support == tmpset.support:
                        if len(closure) <= cl: closure.append(tmpset.suffix)
                        else: closure[cl] = tmpset.suffix
                        cl += 1
                    else: children.append(tmpset)
            
#            if self.output: self.printset(prefix, set1.support, closure[:cl])
#            if self.outfilename: 
            self.saveset(prefix, set1.support, closure[:cl])
            counter += 2**cl
            
            if len(children):
                children.sort()
                counter += self.eclat_mine(children, prefix, closure, cl, depth+1)
            
            prefix.remove(set1.suffix)
            del children
        
        return counter
    
#    def printset(self, prefix, supp, closure=[]):
#        for item in prefix: print item,
#        print '(' + str(supp) + ')'
#        for i, item in enumerate(closure):
#            prefix.append(item)
#            self.printset(prefix, supp, closure[i+1:])
#            prefix.remove(item)
#        return
    
#    def printclosed(self, prefix, supp, closure=[]):
#        """print all 'locally closed' itemsets
#        """
#        for item in prefix: print item,
#        for item in closure: print item,
#        print '(' + str(supp) + ')'
#        return
    
    def saveset(self, prefix, supp, closure=[]):
        self.frequentItemsets.append((prefix[:], supp))
#        print prefix, supp
#        for item in prefix: self.out.write(str(item) + ' ')
#        print '(' + str(supp) + ')'
#        self.out.write('(' + str(supp) + ')' + '\n')
        for i, item in enumerate(closure):
            prefix.append(item)
            self.saveset(prefix, supp, closure[i+1:])
            prefix.remove(item)
        return
    
#    def saveclosed(self, prefix, supp, closure=[]):
#        for item in prefix: self.out.write(str(item) + ' ')
#        for item in closure: self.out.write(str(item) + ' ')
#        self.out.write( '(' + str(supp) + ')' + '\n')
#        return
    
    def getFrequentItemsets(self, maxdepth=0):
#        if self.verbose: 
#            print 'Eclat frequent itemset mining algorithm'
#            print '  implementation by Michael Mampaey'
#            print 'Reading', self.filename, '...', flush,
        self.read_data()
#        self.read_data()
#        if self.verbose: print self.item_count, 'items,', self.trans_count, 'transactions.'
        self.prune_items()
#        if self.verbose:
#            print 'Mining frequent itemsets with minsup=' + str(self.minsup),
#            if self.maxdepth: print 'and maxsize='+str(self.maxdepth),
#            print '...', flush,
#            if self.output: print
#        if self.outfilename: 
#        self.out = file(self.outfilename, 'w')
        self.eclat_mine(self.data)
#        if self.outfilename: 
#        self.out.close()
#        if self.verbose:
#            print 'done.'
#            print f_count, 'frequent itemsets found.'
        itemIdToItemMap = GeneralMethods.reverseDict(self.itemToItemIdMap)
        return [([itemIdToItemMap[itemId] for itemId in itemset[0]], itemset[1]) for itemset in self.frequentItemsets]
    