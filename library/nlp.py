'''
Created on Jun 14, 2011

@author: kykamath
'''

import enchant, re, cjson, os, pprint
from stop_words import stopWords
from nltk.collocations import BigramCollocationFinder
from nltk.probability import FreqDist

current_directory = '/'.join(__file__.split('/')[:-1])
twitter_stop_words_file=current_directory+'/data/stop_words.json'
twitter_stop_words_over_threshold_percentage = 0.5
stopWordsModule = 'stop_words.py'

pattern = re.compile('[\W_]+')
enchantDict = enchant.Dict("en_US")

def isEnglish(sentance, threshold=0.3):
    data = sentance.split()
    englishWords, totalWords = 0.0, len(data)
    try:
        englishWords = sum(1.0 for w in data if len(w)<15 and enchantDict.check(w))
    except Exception: pass
    if englishWords/totalWords > threshold: return True
    return False

def getPhrases(items, minPhraseLength, maxPhraseLength):
    def groupPhrases(items, groups, size):
        itemsLen = len(items)
        for i in range(itemsLen): 
            if i+size<itemsLen+1: groups.append(' '.join(items[i:i+size]))
    groups = [i for i in items if i[0]=='#']
    for size in range(minPhraseLength, maxPhraseLength+1): groupPhrases(items, groups, size)
    return groups

class StopWords:
    set=None
    @staticmethod
    def contains(word, extra_terms=['#p2', '#ff', '#fb', '#followfriday']): 
        if StopWords.set==None: StopWords.set = set(stopWords+extra_terms)
        return word in StopWords.set
    @staticmethod
    def createStopWordsModule():
        outputList=[]
        stop_word_candidates = [t for t in cjson.decode(open(twitter_stop_words_file).readlines()[0]).iteritems()]
        for stop_word_candidate in stop_word_candidates:
            if stop_word_candidate[1]['ot'] >= twitter_stop_words_over_threshold_percentage: outputList.append(stop_word_candidate[0])
        os.system('echo "stopWords=%s" > %s'%(pprint.pformat(outputList), stopWordsModule))
        
def getWordsFromRawEnglishMessage(message, check_stop_words=True):
    returnWords = []
    if isEnglish(message.lower()):
        message = filter(lambda x: not x.startswith('@') and not x.startswith('http:'), message.lower().split())
        for word in message:
            if word[0]=='#': returnWords.append(str('#'+pattern.sub('', word)))
            else: returnWords.append(str(pattern.sub('', word)))
        returnWords = filter(lambda w: len(w)>2, returnWords)
        if check_stop_words: return filter(lambda w: not StopWords.contains(w) and len(w)>2, returnWords)
        else: return filter(lambda w: len(w)>2, returnWords)
    return returnWords

def getCollocations():
    class FeatureAndClassCollocationFinder(BigramCollocationFinder):
        @classmethod
        def from_words(cls, words, window_size=2):
            """Construct a BigramCollocationFinder for all bigrams in the given
            sequence.  By default, bigrams must be contiguous.
            """
            wfd = FreqDist()
            bfd = FreqDist()
    
            if window_size < 2:
                raise ValueError, "Specify window_size at least 2"
    
            for window in classGenerator():
                w1 = window[0]
                try:
                    window = window[:list(window).index(w1, 1)]
                except ValueError:
                    pass
                wfd.inc(w1)
                for w2 in set(window[1:]):
                    if w2 is not None:
                        bfd.inc((w1, w2))
            return cls(wfd, bfd)
    def classGenerator():
        return [('a', 1), ('a', 1), ('b', 2), ('b', 2), ('b', 2)]
    def classGenerator1():
        return ['a', 1, 'a', 1, 'b', 2, 'b', 2,'b', 2]
    
    import nltk
    
    from collections import defaultdict
    
    documents = [('a a a c c c', 1), ('b b b c c c', 2)]
    word_fd = nltk.FreqDist(feature for doc in documents for feature in doc[0].split())
    for document, clusterId in documents:
        if clusterId not in word_fd: word_fd[clusterId]=0
        word_fd[clusterId]+=1
    word_fd
#    word_fd, bigram_fd = defaultdict(int), defaultdict(int)
#    for docVector, clusterId in documents:
#        word_fd[clusterId]+=1
#        for feature, count in docVector.iteritems(): 
#            word_fd[feature]+=count
#            bigram_fd[(feature, clusterId)]+=count
#    print word_fd
#    print bigram_fd
    bigram_fd = nltk.FreqDist((feature, doc[1]) for doc in documents for feature in doc[0].split())

    bigram_measures = nltk.collocations.BigramAssocMeasures()
#    finder = BigramCollocationFinder.from_words(classGenerator1())
#    print finder.nbest(bigram_measures.pmi, 10)  

#    word_fd = nltk.FreqDist(['a', 'a', 'b', 'b', 'b', 1, 2])
#    bigram_fd = nltk.FreqDist([('a', 1), ('a', 1), ('b', 2), ('b', 2), ('b', 2)])
    finder = BigramCollocationFinder(word_fd, bigram_fd)
    scored = finder.score_ngrams(bigram_measures.pmi)
    print scored
#    print sorted(bigram for bigram, score in scored)
if __name__ == '__main__':
#    StopWords.createStopWordsModule()
    getCollocations()
