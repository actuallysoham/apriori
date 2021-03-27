# Soham De
# Tanvi Roy
# Manish Rajani

import csv
from optparse import OptionParser
from itertools import chain, combinations
from tabulate import tabulate
from visualize import *

# For visualisation
supportLookup = dict()
freqLookup = dict()

def powerset(iterable): # modified from https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
    '''
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    '''
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s))))

def getRules(frequentSet):
	'''
	Returns:
	- Tuples with antecedents and consequents
	'''
	powerSet = powerset(frequentSet)
	rules = list()
	for subset in powerSet:
		complementSet = frequentSet.difference(set(subset))
		rules.append((frozenset(subset),frozenset(complementSet)))
		#print(f"{frozenset(subset)} --> {frozenset(complementSet)}")
	return rules

def getConfidence(rule, transactions):
	A = set(rule[0])
	B = set(rule[1])
	confidence = getSupport(A.union(B), transactions)/getSupport(A, transactions)
	return confidence


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
	#print(f"Support for {item} is {freq/len(transactions)}")
	freqLookup[frozenset(item)] = freq
	supportLookup[frozenset(item)] = freq/len(transactions)
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

def getJoin(itemSet):
	'''
	Returns:
	- Frozen set containing the Join of itemSet
	'''
	length = len(list(itemSet)[0]) + 1
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
				#print(item)
				CSet.add(frozenset([item])) # frozenset (unlike a set) is hashable, hence can be a set element
			
			#CSet.add(frozenset(items))
	return rows, CSet


def apriori(data, support, confidence):
	'''
	Prints:
	- Frequent ItemSets
	- Support
	- Confidence
	'''
	transactions, C = getTransactions(data)
	L = []

	while(len(C) > 0):
		newL = getItemsOverSupportThreshold(C, transactions, support)
		if (len(newL) < 1):
			break
		else: 
			L = newL
			C = getJoin(L)


	#print(f"Frequent ItemSets: {L}")
	rules = []
	for item in L:
		rules += getRules(item)

	assocRules = []

	for rule in rules:
		conf = getConfidence(rule, transactions)
		if (conf > confidence):
			assocRules.append([set(rule[0]), set(rule[1]), conf])
			#print(f"{set(rule[0])} --> {set(rule[1])} || Confidence: {conf}")
	
	#print(assocRules)
	print(tabulate(assocRules, headers=['Antecedents', 'Consequents', 'Confidence']))
	visualize(freqLookup)



if __name__ == "__main__":
	'''
	CLI commands for demo:

	python3 apriori.py -d "datafile.csv" -s 0.25 -c 0.75

	python3 apriori.py -s 0.04 -c 0.4 -d groceries.csv
	'''

	optparser = OptionParser()
	optparser.add_option("-d", dest="data", default="data.csv")
	optparser.add_option("-s", dest="support", default=0.4, type="float")
	optparser.add_option("-c", dest="confidence", default=0.0, type="float")
	(options, args) = optparser.parse_args()
	support = options.support
	confidence = options.confidence
	data = options.data
	apriori(data, support, confidence);

