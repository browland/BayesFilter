import sys
from BayesFilter import BayesFilter
import BayesDB

db = BayesDB.createOrLoad(sys.argv[1])
filter = BayesFilter(db)
print filter.predict(sys.argv[2], sys.argv[3])

