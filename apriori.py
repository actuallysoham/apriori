import csv
from optparse import OptionParser

def getSupport(item, transactions):
	freq = 0
	for transaction in transactions:
		flag = 1
		for i in item:
			if i not in transaction: flag = 0
		freq += flag
	print(f"Support for {item} is {freq/len(transactions)}")
	return freq/len(transactions)


def getItemsOverSupportThreshold(CSet, transactions, support):
	prunedSet = set()
	for item in CSet:
		if getSupport(item, transactions) > support:
			# do something
			prunedSet.add(frozenset(item))
			
	return prunedSet

def getJoin(itemSet, length):
	return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])

def getTransactions(data):
	'''
	Returns:
	- Transactions from CSV as a Python List
	- Candidate Set for 1-Itemsets as a Python Set
	'''
	rows = list()
	CSet = set()
	with open(data, newline='') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			rows.append(row)
			for item in row:
				CSet.add(frozenset(item)) # tuple (unlike a list) is hashable, hence can be a set element
	return rows, CSet


def apriori(data, support, confidence):
	transactions, C1 = getTransactions(data)
	print(transactions)
	print(C1)
	L1 = getItemsOverSupportThreshold(C1, transactions, support)
	print(L1)
	C2 = getJoin(L1, 2)
	print(C2)
	L2 = getItemsOverSupportThreshold(C2, transactions, support)
	print(L2)
	C3 = getJoin(L2, 3)
	print(C3)
	L3 = getItemsOverSupportThreshold(C3, transactions, support)
	print(L3)


if __name__ == "__main__":
	'''
	CLI commands for demo:

	python3 apriori.py -d "datafile.csv" -s 0.25 -c 0.75
	'''

	optparser = OptionParser()
	optparser.add_option("-d", dest="data", default="data.csv")
	optparser.add_option("-s", dest="support", default=0.4, type="float")
	optparser.add_option("-c", dest="confidence", default=0.6, type="float")
	(options, args) = optparser.parse_args()
	support = options.support
	confidence = options.confidence
	data = options.data
	apriori(data, support, confidence);
