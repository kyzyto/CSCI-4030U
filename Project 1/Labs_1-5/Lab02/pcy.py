import csv
import numpy as np
import itertools
from collections import Counter
from itertools import combinations
import time

# read retail.dat to a list of lists
datContent = [np.asarray(i.strip().split()).astype(int) for i in open("../retail.dat").readlines()]

supportPercent = 0.05
testSize = 88162 #Whole dataset is 88162

#Get sample size
testSample = np.asarray(datContent[0:testSize])
del datContent

def logical_xor(val1, val2, numBaskets):
    return ((val1) ^ (val2)) % numBaskets

#Dictionaries Definition / lists
singleDict = dict()
doubleBitVector = dict.fromkeys(range(20000), 0)
currDoubles = []
validDoubles = dict()
validSingles = dict()
doubleCount = dict()
skimmedSample = []

#Compute Support
support = int(len(testSample) * supportPercent)
print("Support ", support)

start = time.time()
#First Pass
#Count singles and hash pairs to hashtable
for basket in testSample:
    doubleCands = []
    for single in basket:
        if single in singleDict:
            singleDict[single] += 1
        else:
            singleDict[single] = 1

    comb = combinations(basket, 2)
    for double in list(comb):
        doubleBitVector[logical_xor(double[0], double[1], 20000)] += 1

#Translate count of hashtable values to (0 or 1) depending on support
for key, value in doubleBitVector.items():
    if value >= support:
        doubleBitVector[key] = 1
    else:
        doubleBitVector[key] = 0

#Find singles which meet support
for key, values in singleDict.items():
    if(values > support):
        validSingles[key] = values

#Show valid singles and create double candidates
singleKeys = set(validSingles.keys())
print("Singles")
print(singleKeys)
print(len(singleKeys))
singlePairs = combinations(singleKeys, 2)
for double in list(singlePairs):
    doubleCount[(double[0], double[1])] = 0

#Second Pass
#Count basket pairs if they hash to a valid bucket
for basket in testSample:
    comb = combinations(basket, 2)
    for double in list(comb):
        hashed = doubleBitVector[logical_xor(double[0], double[1], 20000)]
        if hashed == 1 and doubleCount.get(double) != None:
            #if doubleCount.get(double) != None:
            doubleCount[double] += 1

#Find double pairs which meet support and create a table
for (key), value in doubleCount.items():
    if value >= support:
        validDoubles[key] = value
print("Doubles")
print(set(validDoubles.keys()))
print(len(validDoubles))
end = time.time()
print("Time taken: ", end - start, " seconds.")

"""
Support  4408
Singles
{32, 65, 38, 39, 41, 48}
6
Doubles
{(38, 39), (32, 39), (41, 48), (32, 48), (39, 48), (38, 48), (39, 41)}
7
Time taken:  11.692109107971191  seconds.
"""
