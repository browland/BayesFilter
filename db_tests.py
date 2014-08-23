import BayesDB

## create a DB via the constructor which always creates a new BayesDB file
db = BayesDB.BayesDB()
db.addDoc("offer is secret", "spam")
db.dump()

## load() looks for file called 'BayesDB' by default
db = BayesDB.load()
db.describe()

