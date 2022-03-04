import csv
import numpy as np
import itertools
from collections import Counter
from itertools import combinations
import time

# read retail.dat to a list of lists
datContent = [np.asarray(i.strip().split()).astype(int) for i in open("../retail.dat").readlines()]

supportPercent = 0.05
testSize = 88126 #Whole dataset is 88126
sampleSize = 5000

#Get sample size
testSample = np.asarray(datContent[0:testSize])
testSample = np.random.choice(testSample, sampleSize)
print(len(testSample))
del datContent

#Define required dictionaries / counters / lists
cnt = Counter()
doubleCandidates = dict()
skimmedSample = []
doubleCount = dict()
validDoubles= dict()

#Compute support
support = int(len(testSample) * supportPercent)
print("Support ", support)


start = time.time()

#First Pass
#Count singles
for i in list(itertools.chain.from_iterable(testSample)):
    cnt[i] +=1
singles = dict(cnt)
#print(singles)

#Find singles which meet support
for key, values in singles.items():
    if(values > support):
        doubleCandidates[key] = values

singleKeys = set(doubleCandidates.keys())
print("Singles")
print(doubleCandidates)
print(len(doubleCandidates))

"""Optional Data skimming
for basket in testSample:
    if len(set(basket).intersection(singleKeys)) > 0:
        skimmedSample.append(basket)
"""
#Create double candidates
doubles = itertools.combinations(doubleCandidates, 2)

doubleFreq = []

#Generate double candidates
singlePairs = combinations(doubleCandidates, 2)
for double in list(singlePairs):
    doubleCount[(double[0], double[1])] = 0

for basket in testSample:
    comb = combinations(basket, 2)
    for double in list(comb):
        if doubleCount.get(double) != None:
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
5000
Support  250
Singles
{39: 2867, 48: 2327, 38: 871, 41: 828, 32: 841}
5
Doubles
{(39, 48), (39, 41)}
2
Time taken:  0.12253975868225098  seconds.
"""
