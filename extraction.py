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
        positiveAllowed = [max(inputList)] if max(inputList) not in [-1, 0, 1] else [999]
        negativeAllowed = [min(inputList)] if min(inputList) not in [-1, 0, 1] else [-999]

    elif type == 'Percentile':
        positiveAllowed = [x for x in inputList if x >= np.percentile(inputList, 80) and x not in [-1, 0, 1]]
        negativeAllowed = [x for x in inputList if x <= np.percentile(inputList, 20) and x not in [-1, 0, 1]]

    outputAspects = []

    print(rangesDict.items())

    textSpansPositive = [(x, y) for ((x, y), v) in rangesDict.items() if v in positiveAllowed and x-y > 3]
    textSpansNegative = [(x, y) for ((x, y), v) in rangesDict.items() if v in negativeAllowed and x-y > 3]

    print(textSpansPositive)

    textSpansPositive = [((x, y), 'positive') for (x, y) in textSpansPositive]
    textSpansNegative = [((x, y), 'negative') for (x, y) in textSpansNegative]
    textSpans = textSpansPositive + textSpansNegative

    for span, sentiment in textSpans:
        start, end = span
        outputAspects.append((text[start:end], sentiment))


    return textSpans, outputAspects

def isOverlapping(trueSpan, predSpan):
  startTrue, endTrue = trueSpan
  startPred, endPred = predSpan

  if startPred < startTrue:
    startTrue, endTrue = predSpan
    startPred, endPred = trueSpan

  return bool(range(max(startTrue, startPred), min(endTrue, endTrue)+1))
