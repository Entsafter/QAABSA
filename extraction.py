from collections import Counter
import numpy as np


test_text = "The tree is great"
test = [1, 1, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0 , 0, 0, 0]

def createRanges(inputList):
    outputDict = {}

    for index, value in enumerate(inputList):

        if index == len(inputList)-1:
            outputDict[(start, index+1)] = value

        elif index == 0:
            start = 0

        elif inputList[index] != inputList[index+1]:
            outputDict[(start, index+1)] = value
            start = index + 1

    return outputDict


def getAspectSpans(inputDict, text, type='MinMax'):

    inputList = [v for (k, v) in inputDict.items()]
    rangesDict = createRanges(inputList)

    if type == 'MinMax':
        allowed = [max(inputList), min(inputList)]

    elif type == 'Percentile':
        allowed = [x for x in inputList if (x <= np.percentile(inputList, 20) or x >= np.percentile(inputList, 80)) and x not in [-1, 0, 1]]



    outputAspects = []

    textSpans = [k for (k, v) in rangesDict.items() if v in allowed and v != 0]

    for start, end in textSpans:
        outputAspects.append(text[start:end])

    return textSpans, outputAspects
