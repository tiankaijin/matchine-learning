from math import log
''' prepare dataset'''
def createDataSet():
    dataset = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],
    [0,1,'no']]
    labels=['no surfacing','flippers']
    return dataset,labels

'''calc shannonEnt'''
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLable = featVec[-1]
        if currentLable not in labelCounts.keys():
            labelCounts[currentLable]=0
        labelCounts[currentLable]+=1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -=prob * log(prob,2)
    return shannonEnt
'''split
@dataset:data
@axis:characteristic
@value:characteristic's value
'''
def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reduceDeatVec = featVec[:axis]
            reduceDeatVec.extend(featVec[axis+1:])
            retDataSet.append(reduceDeatVec)
    return retDataSet

'''choose max'''
def chooseBestFeatureToSplit(dataSet):
    numFeature=len(dataSet[0])-1
    baseEntropy = calcShannonEnt(dataSet)
    bestIG = 0
    bestFeature = -1
    for i in range(numFeature):
        featList=[number[i] for number in dataSet]
        uniqualVals=set(featList)
        newEntropy=0
        for value in uniqualVals:
            subDataSet=splitDataSet(dataSet,i,value)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestIG):
            bestIG = infoGain
            bestFeature = i
    return bestFeature

import operator
def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys:classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount = sorted(classCount.items(),key = operator.itemgetter(1),reversed = True)
    return sortedClassCount
def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[-1]) == len(classList):
        return classList[-1]
    if (len(classList[0]) == 1):
        print("aaaaaaaaa")#never used
        return majorityCnt(classList)
    
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels=labels[:]
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
        print (labels)
       
    return myTree
def classify(inputTree,feeatLabels,testVec):
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = feeatLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if(type(secondDict[key]).__name__=='dict'):
                classLabel = classify(secondDict[key],feeatLabels,testVec)
            else:classLabel = secondDict[key]
    return classLabel
def storeTree(inputTree,filename):
    import pickle
    fw = open(filename,'wb')
    pickle.dump(inputTree,fw)
    fw.close
def grabTree(filename):
    import pickle
    fr = open(filename,'rb')
    return pickle.load(fr)

ds ,label= createDataSet()
res = calcShannonEnt(ds)
mtree = createTree(ds,label)
storeTree(mtree,"tkj.txt")
tr = grabTree('tkj.txt')
label=['no surfacing','flippers']
print (tr)
print (classify(tr,label,[0,0]))






