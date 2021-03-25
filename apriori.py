import csv
from optparse import OptionParser

def getSupport(item, transactions):
	'''
	Returns:
	- Support for item in transactions
	'''
	freq = 0
	for transaction in transactions:
		flag = 1
		for i in item:
			if i not in transaction: flag = 0
		freq += flag
	print(f"Support for {item} is {freq/len(transactions)}")
	return freq/len(transactions)


def getItemsOverSupportThreshold(CSet, transactions, support):
	'''
	Returns:
	- Subset of CSet with support above threshold
	'''
	prunedSet = set()
	for item in CSet:
		if getSupport(item, transactions) > support:
			prunedSet.add(frozenset(item))
			
	return prunedSet

def getJoin(itemSet, length):
	'''
	Returns:
	- Frozen set containing the Join of itemSet
	'''
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
				CSet.add(frozenset(item)) # frozenset (unlike a set) is hashable, hence can be a set element
	return rows, CSet


def apriori(data, support, confidence):
	'''
	Returns:
	- Frequent ItemSets
	- Support
	- Confidence (TBD)
	'''
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
	
    # Generate association rules from the frequent itemsets

	assocRules = dict()
    # Dictionary which stores Association Rules

	largeSet = dict()
    # Global dictionary which stores (key = n-itemSets, value = support)
    # which satisfy minimum support

    currentLSet = prunedSet

    k = 2 
    while currentLSet != set([]): # generalising 
    	currentLSet = getJoin(currentLSet, k)
    	currentCSet = getItemsOverSupportThreshold(currentLSet, transactionList, minSupport)
    	currentLSet = currentCSet
    	k = k + 1

	getItems = []
	for key, value in largeSet.items():
		getItems.extend([(tuple(item), getSupport(item)) for item in value])

	getRules = []
	for key, value in list(largeSet.items())[1:]:
		for item in value:
			_subsets = map(frozenset, [x for x in subsets(item)])
			for element in _subsets:
				remain = item.difference(element)
				if len(remain) > 0:
					confidenceCalculated = getSupport(item) / getSupport(element)
					if confidenceCalculated >= confidence:
						getRules.append(((tuple(element), tuple(remain)), confidenceCalculated))
	return getItems, getRules

	# Confidence(A->B) = Support_count(A∪B)/Support_count(A)

	print("Rules generated")
	print(getRules)


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

'''
Things that are pending:
- Confidence Calculation
- Association Rules Generation
- Pruning on Confidence Threshold
- Visualisation (whatever Mondal means by that)
- Dataset generation
'''
