class BayesDB:

    ## **************
    ## *** Fields ***
    ## **************

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

