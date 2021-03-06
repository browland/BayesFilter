from BayesDB import BayesDB

class BayesFilter:

    ## **************
    ## *** Fields ***
    ## **************

    ## All the word frequency tables etc.
    db = None

    ## Laplace Smoothing parameter - prevents over-fitting.
    ## Over-fitting will mean a document will never fit a particular class,
    ## unless all of its words were seen at least once in the training data
    ## for that class.
    k = 1

    ## **********************
    ## *** Public Methods ***
    ## **********************

    def predict(self, label, doc):
        """
        Probability of the doc belonging to class 'label'.
        """
        if label not in self.db.labelToDocsCount.keys():
            print "unknown label %s" % label
            exit()

        probDocGivenLabel =  self.__probDocGivenLabel(doc, label)
        probLabel = self.__probLabel(label)
        probDoc = self.__probDoc(doc, label)
        return float(probDocGivenLabel * probLabel) / probDoc

    ## ***********************
    ## *** Private Methods ***
    ## ***********************

    def __init__(self, db):
        self.db = db

    def __freqInDict(self, word, dict):
        if word not in dict:
            return 0
        else:
            return dict[word]

    def __probLabel(self, label):
        """
        Probability of a label occurring in a random document.
        """
        if label not in self.db.labelToDocsCount.keys():
            print "Error: label %s not in DB" % label
            exit()

        # Use Laplacian smoothing
        return float(self.db.labelToDocsCount[label] + 1) / (self.db.allDocsCount + 2)

    def __probNotLabel(self, label):
        """
        Probability of label not occurring in a random document.
        """
        return 1 - self.__probLabel(label)

    def __probWordGivenLabel(self, word, label):
        """
        Probability of encountering 'word', given it belongs to class 'label'.
        """
        ## Get no. of occurrences of word in label
        if word not in self.db.labelToWordToFreq[label]:
            freqInLabel = 0
        else:
            freqInLabel = self.db.labelToWordToFreq[label][word]

        ## Get total count of words in label
        totalWordCountInLabel = sum(self.db.labelToWordToFreq[label].values())

        ## Find probability of word coming up in class 'label', using Laplace Smoothing
        return float(freqInLabel + self.k) / (totalWordCountInLabel + (self.k * len(self.db.wordToTotalFreq)))

    def __probWordGivenNotLabel(self, word, label):
        """
        Probability of encountering 'word', given it does not belong to class 'label'.
        """
        ## Get no. of occurrences of word not in label
        if word not in self.db.wordToTotalFreq.keys():
            totalOccurrences = 0
        else:
            totalOccurrences = self.db.wordToTotalFreq[word]

        ## Get no. of occurrences of word IN label
        if word not in self.db.labelToWordToFreq[label]:
            freqInClass = 0
        else:
            freqInClass = self.db.labelToWordToFreq[label][word]

        occurrencesNotInClass = totalOccurrences - freqInClass

        ## Get total count of words not in clazz
        totalWordCountNotInClazz = self.db.totalWordCount - sum(self.db.labelToWordToFreq[label].values())

        ## Find probability of word coming up in clazz, using Laplace Smoothing with k = 1
        return float(occurrencesNotInClass + 1) / (totalWordCountNotInClazz + len(self.db.wordToTotalFreq))

    def __probDocGivenLabel(self, doc, label):
        """
        Probability of encountering doc given it belongs to label.  N.B. this is the converse
        of what predict() does (which finds the probability of a label given we encountered 'doc').
        """
        product = 1
        for word in doc.split():
            word = word.lower()
            product *= self.__probWordGivenLabel(word, label)
        return product

    def __probDocGivenNotLabel(self, msg, label):
        """
        Probability of encountering doc given it does not belong to label.
        """
        product = 1
        for word in msg.split():
            word = word.lower()
            product *= self.__probWordGivenNotLabel(word, label)
        return product

    def __probDoc(self, doc, label):
        """
        Total probability of encountering doc either with or without 'label'.
        """
        total = self.__probDocGivenLabel(doc, label) * self.__probLabel(label)\
        + self.__probDocGivenNotLabel(doc, label) * self.__probNotLabel(label)
        return total


