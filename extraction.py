from collections import Counter


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


def getAspectSpans(inputDict, text, type='MaxMin'):

    inputList = [v for (k, v) in inputDict.items()]
    rangesDict = createRanges(inputList)

    if type == 'MaxMin':
        outputAspects = []
        listMax = max(inputList)
        listMin = min(inputList)
        textSpans = [k for (k, v) in rangesDict.items() if v in [listMax, listMin]]

        for start, end in textSpans:
            outputAspects.append(text[start:end])

    return outputAspects
