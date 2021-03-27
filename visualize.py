from collections import OrderedDict
import matplotlib.pyplot as plt
import math
import random
from mpl_toolkits.mplot3d import Axes3D

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

def plot3d(freqLookup, supportLookup):
	x_plot=[]
	y_plot=[]
	z_plot=[]
	
	newDict = dict(sorted(freqLookup.items(), key=lambda item: item[1]))
	freqLookup = OrderedDict(reversed(list(newDict.items())))
	i=0
	for key in freqLookup:
		strn=""
		for j in key:
			strn=strn+j+", "
		x_plot.append(strn)
		y_plot.append(freqLookup[key])
		z_plot.append(supportLookup[key])


		
		# if(freqList[len(key)-1]==None):
		# 	freqList.append([])
		# freqList[len(key)-1].append((key,freqLookup[key]))
	y_plot_set=set(y_plot)
	y_plot_set=list(y_plot_set)
	y_plot_set.reverse()

	colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(y_plot_set))]
	
	colorList=[colors[y_plot_set.index(i)] for i in y_plot]
	fig = plt.figure()
	

	ax=Axes3D(fig)
	ax.scatter(range(0,len(freqLookup)),y_plot,z_plot)
	ax.set_xlabel('Itemset number')
	ax.set_ylabel('Frequency')
	ax.set_zlabel('Support')
	plt.show()