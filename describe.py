import sys
from BayesFilter import BayesFilter
import BayesDB

db = BayesDB.createOrLoad('out')
print db.describe()

