import csv
from optparse import OptionParser
from collections import OrderedDict
from itertools import chain, combinations
import matplotlib.pyplot as plt
import math
import random

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
				CSet.add(frozenset(item)) # frozenset (unlike a set) is hashable, hence can be a set element
	return rows, CSet


def apriori(data, support, confidence):
	'''
	Prints:
	- Frequent ItemSets
	- Support
	- Confidence
	'''
	transactions, C = getTransactions(data)

	while(len(C) > 0):
		L = getItemsOverSupportThreshold(C, transactions, support)
		#print(L)
		C = getJoin(L)
		if (len(C) == 1):
			L = C
			break

	print(f"Frequent ItemSets: {L}")

	for item in L:
		rules = getRules(item)

	for rule in rules:
		conf = getConfidence(rule, transactions)
		if (conf > confidence):
			print(f"{rule[0]} --> {rule[1]} || Confidence: {conf}")

def visualize(freqLookup):
	x_plot=[]
	y_plot=[]
	newDict = dict(sorted(freqLookup.items(), key=lambda item: item[1]))
	freqLookup = OrderedDict(reversed(list(newDict.items())))
	for key in freqLookup:
		print("Key = ",key,"|| Val = ",freqLookup[key],"|| Length=",len(key))
		strn=""
		for j in key:
			strn=strn+j+", "
		print(strn)
		x_plot.append(strn)
		y_plot.append(freqLookup[key])
		# if(freqList[len(key)-1]==None):
		# 	freqList.append([])
		# freqList[len(key)-1].append((key,freqLookup[key]))
	y_plot_set=set(y_plot)
	y_plot_set=list(y_plot_set)
	y_plot_set.reverse()
	print(y_plot_set)

	colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(y_plot_set))]
	print(x_plot,y_plot)
	colorList=[colors[y_plot_set.index(i)] for i in y_plot]
	fig = plt.figure()
	plt.bar(x_plot,y_plot,color=colorList)
	plt.xlabel("Itemset")
	plt.ylabel("Frequency")

	plt.show()

if __name__ == "__main__":
	'''
	CLI commands for demo:

	python3 apriori.py -d "datafile.csv" -s 0.25 -c 0.75
	'''

	optparser = OptionParser()
	optparser.add_option("-d", dest="data", default="data.csv")
	optparser.add_option("-s", dest="support", default=0.4, type="float")
	optparser.add_option("-c", dest="confidence", default=0.7, type="float")
	(options, args) = optparser.parse_args()
	support = options.support
	confidence = options.confidence
	data = options.data
	apriori(data, support, confidence)
	print("=========================")


	visualize(freqLookup)
'''
Things that are pending:
- Visualisation (whatever Mondal means by that)
- Dataset generation
- Some Optimisations are Possible
'''
