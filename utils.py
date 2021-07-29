from math import floor, ceil
import requests

def find_sub_list(sl,l):
    sll=len(sl)
    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            return ind,ind+sll-1

def britishize(string):
    url ="https://raw.githubusercontent.com/hyperreality/American-British-English-Translator/master/data/american_spellings.json"
    american_to_british_dict = requests.get(url).json()

    for american_spelling, british_spelling in american_to_british_dict.items():
        string = string.replace(american_spelling, british_spelling)

    return string

def combineDicts(dictList):
  finalDict = {k:0 for k in range(0, max(dictList[0])+1)}
  for dictElement in dictList:
    for key, value in dictElement.items():
      finalDict[key] += value

  # norm
  finalDict = {k:v/len(dictList) for (k, v) in finalDict.items()}

  return finalDict

def ceilFloor(x):
    """Returns the floor for positive numbers, the ceil for negative numbers."""
    if x > 0:
        return floor(x)
    else:
        return ceil(x)

def cutOff(x, max_, min_):
    """Cuts off values larger than the maximum or smaller than the minimum and
        returns the maximum/minimum."""
    if x > max_:
        return max_
    elif x < min_:
        return min_
    else:
        return x
