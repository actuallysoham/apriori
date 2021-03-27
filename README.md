# apriori
Implementation of Association Rule Mining Algorithms

## Getting Started

Open up your terminal and type the following commands. The **-d** flag stands for the csv file datasource, the **-s** flag stands for the minimum support threshold and the **-c** flag is for minimum confidence. You may omit the **-c** flag if you want the full list of all rules. Other flags also have defaults The following are some sample commands

```
python3 apriori.py -s 0.4 -c 0.6 -d data2.csv 
python3 apriori.py -s 0.1 -c 0.6 -d data6.csv 
python3 apriori.py -s 0.04 -c 0.4 -d groceries.csv 
python3 apriori.py -s 0.04 -d groceries.csv 
```
## Visualisations

The following visualisations are provided in **visualize.py**:

* Frequency Plot (of all Itemsets)
* 3D Plot {x: Itemset Number, y: Frequency, z: Confidence}

## Datasets
The current test data sources are **data.csv** and **groceries.csv**. The later has **169 distinct items and ~10,000 transactions**.
