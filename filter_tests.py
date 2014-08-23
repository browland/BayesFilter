from BayesFilter import BayesFilter
from BayesDB import BayesDB

## Example data taken from Stanford AI video class (Unit 5 Machine Learning)
## http://www.ai-class.org

db = BayesDB()
filter = BayesFilter(db)

## Add some messages we flagged as spam
db.addDoc("offer is secret", "spam")
db.addDoc("click secret link", "spam")
db.addDoc("secret sports link", "spam")

## Add some messages we did not flag
db.addDoc("play sports today", None)
db.addDoc("went play sports", None)
db.addDoc("secret sports event", None)
db.addDoc("sports is today", None)
db.addDoc("sports costs money", None)

print "Probability of spam, given message 'today is secret' = %s" % filter.predict("spam", "today is secret")

