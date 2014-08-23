import sys 
import BayesDB

classifier = sys.argv[1].strip()
if classifier == 'NONE':
    classifier = None

training_data = open(sys.argv[2], 'r')
db_file = sys.argv[3]
db = BayesDB.createOrLoad(db_file)

docs = 0
for line in training_data:
    line = line.strip()

    ## assume non-trivial sanitisation done upstream
    if line == "":
        continue

    db.addDoc(line, classifier)
    docs+=1

print 'Classified %d docs as %s' % (docs, classifier)
print 'Writing DB file %s ...' % db_file
db.dump()
print 'New DB state:'
db.describe()
print 'Done'
