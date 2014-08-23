import pickle
import os.path

class BayesDB:

    ## **************
    ## *** Fields ***
    ## **************
    dbFile                = None

    ## Frequency tables and related book-keeping
    wordToTotalFreq       = {}
    labelToWordToFreq     = {}
    labelToDocsCount      = {}
    totalWordCount        = 0
    allDocsCount          = 0

    ## **********************
    ## *** Public Methods ***
    ## **********************

    def addDoc(self, doc, label):
        """
        Adds a doc (just a string) to the DB.  Label is optional (if this
        doc is not labelled then just pass None).  Calling this method will
        update the probabilities according to the words in the document, and
        the presence/absence of a label.
        """
        self.allDocsCount+=1

        for word in doc.split():
            self.__addWord(word)

        if label:
            self.__labelDoc(label, doc)

    ## ***********************
    ## *** Private Methods ***
    ## ***********************

    def __init__(self, dbFile='BayesDB'):
        self.dbFile = dbFile

    def __getstate__(self):
        state = {}
        state['dbFile'] = self.dbFile
        state['wordToTotalFreq'] = self.wordToTotalFreq
        state['labelToWordToFreq'] = self.labelToWordToFreq
        state['labelToDocsCount'] = self.labelToDocsCount
        state['totalWordCount'] = self.totalWordCount
        state['allDocsCount'] = self.allDocsCount
        return state

    def __setstate__(self, state):
        self.dbFile = state['dbFile']
        self.wordToTotalFreq = state['wordToTotalFreq']
        self.labelToWordToFreq = state['labelToWordToFreq']
        self.labelToDocsCount = state['labelToDocsCount']
        self.totalWordCount = state['totalWordCount']
        self.allDocsCount = state['allDocsCount']

    def __labelDoc(self, label, doc):
        ## Init label->docs if not already seen
        if label not in self.labelToDocsCount.keys():
            self.labelToDocsCount[label] = 0
        self.labelToDocsCount[label]+=1

        for word in doc.split():
            ## Initialise label->word->freq if not already seen
            if label not in self.labelToWordToFreq.keys():
                self.labelToWordToFreq[label] = {}

            ## Increment word frequency for this label
            if word not in self.labelToWordToFreq[label].keys():
                self.labelToWordToFreq[label][word] = 1
            else:
                self.labelToWordToFreq[label][word] += 1

    def __addWord(self, word):
        if word not in self.wordToTotalFreq:
            self.wordToTotalFreq[word] = 1
        else:
            self.wordToTotalFreq[word] += 1
            
        self.totalWordCount += 1

    def dump(self):
        out = open(self.dbFile, 'wb')
        pickle.dump(self, out)
        out.close()

    def describe(self):
        print 'Classified Word Freqs: %s' % self.labelToWordToFreq
        print 'Classified  Docs: %s' % self.labelToDocsCount
        print 'Total Words: %s' % self.totalWordCount
        print 'Total Docs: %s' % self.allDocsCount

def createOrLoad(dbFile='BayesDB'):
    if os.path.isfile(dbFile):
        print 'DB file exists, loading ...'
        return load(dbFile)
    else:
        print 'No DB file %s found, will create it when necessary.' % dbFile
        return BayesDB(dbFile)

def load(dbFile='BayesDB'):
    input = open(dbFile, 'rb')
    return pickle.load(input)
    input.close()
