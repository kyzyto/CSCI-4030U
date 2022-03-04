import csv
import numpy as np
import itertools
import random
from collections import Counter
from itertools import combinations
import time

# read retail.dat to a list of lists
datContent = [np.asarray(i.strip().split()).astype(int) for i in open("../retail.dat").readlines()]

supportPercent = 0.05
testSize = 88162 #Whole dataset is 88126
numSubSamples = 20

#Get sample size and shuffle it before taking sub-samples
testSample = np.asarray(datContent[0:testSize])
random.shuffle(testSample)

samples = np.asarray(np.array_split(testSample,numSubSamples))

del datContent

#Define required dictionaries / counters / lists

skimmedSample = []
doubleCount = dict()


#Compute support
support = int(len(samples[0]) * supportPercent)
print("Support ", support)

singleTotal = []

start = time.time()

#First Pass
for sample in samples:
    cnt = Counter()
    doubleCandidates = dict()
    #First Pass
    #Count singles
    for i in list(itertools.chain.from_iterable(sample)):
        cnt[i] +=1
    singles = dict(cnt)
    #print(singles)

    #Find singles which meet support
    for key, values in singles.items():
        if(values > support):
            doubleCandidates[key] = values

    singleKeys = set(doubleCandidates.keys())
    singleTotal.extend(singleKeys)

#Remove duplicates to create double candidates
singleTotal = list(dict.fromkeys(singleTotal))
print("Singles")
print(singleTotal)
print(len(singleTotal))

#Create double candidates
singlePairs = combinations(doubleCandidates, 2)
for double in list(singlePairs):
    doubleCount[(double[0], double[1])] = 0

sampledDouble = []
for i in range(len(samples)):
    sampledDouble.append(doubleCount)

doubleTotal = []
#Second Pass
for i in range(len(samples)):
    validDoubles= dict()
    for basket in samples[i]:
        comb = combinations(basket, 2)
        for double in list(comb):
            if sampledDouble[i].get(double) != None:
                sampledDouble[i][double] += 1

    #Find double pairs which meet support and create a table
    for (key), value in sampledDouble[i].items():
        if value >= support:
            validDoubles[key] = value
    doubleTotal.extend(validDoubles)
#Remove duplicates to create final doubles
doubleTotal = list(dict.fromkeys(doubleTotal))
print("Doubles")
print(doubleTotal)
print(len(doubleTotal))
end = time.time()
print("Time taken: ", end - start, " seconds.")
"""
Support  220
Singles
[32, 65, 38, 39, 41, 48]
6
Doubles
[(32, 39), (32, 48), (38, 39), (38, 48), (39, 41), (39, 48), (41, 48), (32, 38), (32, 41), (38, 41), (39, 65), (48, 65), (41, 65), (32, 65), (38, 65)]
15
Time taken:  2.1882684230804443  seconds.
"""
