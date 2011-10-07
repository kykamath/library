#!/usr/bin/python
#
# Python implementation of the Eclat frequent itemset mining algorithm.
# See "New algorithms for fast discovery of association rules" by Zaki et al.
# for details.
# Implementation by Michael Mampaey,  version 0.1.20091008.
#

from classes import GeneralMethods

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
        self.transactionIterator = transactionIterator
        self.minsup      = minsup
        self.item_count  = 0
        self.trans_count = 0
        self.maxdepth    = maxdepth
        self.data        = None
        self.frequentItemsets = []
        self.itemToItemIdMap = {}
    
    def read_data(self):
        """Read data and return list of itemsets, in vertical format
        """
        self.item_count  = 0
        self.trans_count = 0
        self.data = []
        self.data.append(Itemset(0))
        
        for itemset in self.transactionIterator:
            self.trans_count += 1
            for item in itemset:
                if item not in self.itemToItemIdMap: self.itemToItemIdMap[item]=len(self.itemToItemIdMap)+1
                item = self.itemToItemIdMap[item]
                if item > self.item_count:
                    for i in range(self.item_count+1, item+1): self.data.append(Itemset(i))
                    self.item_count = item
                self.data[item].tids.add(self.trans_count)
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
            self.saveset(prefix, set1.support, closure[:cl])
            counter += 2**cl
            
            if len(children):
                children.sort()
                counter += self.eclat_mine(children, prefix, closure, cl, depth+1)
            
            prefix.remove(set1.suffix)
            del children
        
        return counter
    
    def saveset(self, prefix, supp, closure=[]):
        self.frequentItemsets.append((prefix[:], supp))
        for i, item in enumerate(closure):
            prefix.append(item)
            self.saveset(prefix, supp, closure[i+1:])
            prefix.remove(item)
        return
    
    def getFrequentItemsets(self, maxdepth=0):
        self.read_data()
        self.prune_items()
        self.eclat_mine(self.data)
        itemIdToItemMap = GeneralMethods.reverseDict(self.itemToItemIdMap)
        return [([itemIdToItemMap[itemId] for itemId in itemset[0]], itemset[1]) for itemset in self.frequentItemsets]
    