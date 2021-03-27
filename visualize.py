from collections import OrderedDict
import matplotlib.pyplot as plt
import math
import random

def visualize(freqLookup):
	x_plot=[]
	y_plot=[]
	newDict = dict(sorted(freqLookup.items(), key=lambda item: item[1]))
	freqLookup = OrderedDict(reversed(list(newDict.items())))
	for key in freqLookup:
		#print("Key = ",key,"|| Val = ",freqLookup[key],"|| Length=",len(key))
		strn=""
		for j in key:
			strn=strn+j+", "
		#print(strn)
		x_plot.append(strn)
		y_plot.append(freqLookup[key])
		# if(freqList[len(key)-1]==None):
		# 	freqList.append([])
		# freqList[len(key)-1].append((key,freqLookup[key]))
	y_plot_set=set(y_plot)
	y_plot_set=list(y_plot_set)
	y_plot_set.reverse()
	#print(y_plot_set)

	colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(y_plot_set))]
	#print(x_plot,y_plot)
	colorList=[colors[y_plot_set.index(i)] for i in y_plot]
	fig = plt.figure()
	plt.bar(x_plot,y_plot,color=colorList)
	plt.xlabel("Itemset")
	plt.ylabel("Frequency")

	plt.show()
