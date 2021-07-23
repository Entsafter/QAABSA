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


def getAspectSpans(inputDict, text, maxScore, excludePercentage, type='MinMax'):

    inputList = [v/maxScore for (k, v) in inputDict.items()]
    rangesDict = createRanges(inputList)
    excludeMin = -excludePercentage
    excludeMax = excludePercentage


    if type == 'MinMax':
        positiveAllowed = [max(inputList)] if (max(inputList)/maxScore < excludeMin and max(inputList)/maxScore > excludeMax) else [999]
        negativeAllowed = [min(inputList)] if (max(inputList)/maxScore < excludeMin and max(inputList)/maxScore > excludeMax) else [-999]

    elif type == 'Percentile':
        positiveAllowed = [x for x in inputList if x >= np.percentile(inputList, 80) and (max(inputList) < excludeMin and max(inputList) > excludeMax)]
        negativeAllowed = [x for x in inputList if x <= np.percentile(inputList, 20) and (max(inputList) < excludeMin and max(inputList) > excludeMax)]

    outputAspects = []


    textSpansPositive = [((x, y), 'positive', v) for ((x, y), v) in rangesDict.items() if v in positiveAllowed and y-x > 3]
    textSpansNegative = [((x, y), 'negative', v) for ((x, y), v) in rangesDict.items() if v in negativeAllowed and y-x > 3]

    textSpans = textSpansPositive + textSpansNegative

    for span, sentiment in textSpans:
        start, end = span
        outputAspects.append((text[start:end], sentiment))

    print(textSpans, outputAspects)


    return textSpans, outputAspects

def isOverlapping(trueSpan, predSpan):
  startTrue, endTrue = trueSpan
  startPred, endPred = predSpan

  if startPred < startTrue:
    startTrue, endTrue = predSpan
    startPred, endPred = trueSpan

  return bool(range(max(startTrue, startPred), min(endTrue, endTrue)+1))
