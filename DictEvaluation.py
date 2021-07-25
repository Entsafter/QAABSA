from QAABSA.utils import ceilFloor, cutOff, combineDicts
from QAABSA.DictScaling import linearScaleDict, cufOffScaleDict, cufOffRoundScaleDict
import aspect_based_sentiment_analysis as absa

def countOccurences_1_1(positive_answers, negative_answers, text, scaleType):

  # Create list with all indices of the string
  answerIndices = list(range(0, len(text)))

  # Counting number of occurences
  scoreDict = {}

  # Calculate positive scores
  for element in answerIndices:
    scoreDict[element] = 0
    for answer in positive_answers:
      if element in range(answer['start'], answer['end']):
        scoreDict[element] += 1

  for element in answerIndices:
    for answer in negative_answers:
      if element in range(answer['start'], answer['end']):
        scoreDict[element] -= 1

  # Scale and return
  if scaleType == "linearScale":
    return linearScaleDict(scoreDict, 10, -10)
  elif scaleType == "cutOff":
    return cufOffScaleDict(scoreDict, 10, -10)
  elif scaleType == 'cutOffRound':
    return cufOffRoundScaleDict(scoreDict, 10, -10)

def countOccurenceswithABSA_1_1(positive_answers, negative_answers, text, scaleType, nlp_sentiment):

    # Create list with all indices of the string
    answerIndices = list(range(0, len(text)))

    # Counting number of occurences
    scoreDict = {}
    # Calculate positive scores
    for element in answerIndices:
      scoreDict[element] = 0

    if type(positive_answers) is not list:
      positive_answers = [positive_answers]
      negative_answers = [negative_answers]

    for answer in positive_answers:
        # Checking if the sentiment is positive
        sentiment_answer, _ = nlp_sentiment(text=text, aspects=[answer['answer'], 'none'])

        for element in scoreDict:
            if element in range(answer['start'], answer['end']) and sentiment_answer.sentiment == absa.Sentiment.positive:
                scoreDict[element] += 1

    for answer in negative_answers:
        sentiment_answer, _ = nlp_sentiment(text=text, aspects=[answer['answer'], 'none'])

        for element in scoreDict:
            if element in range(answer['start'], answer['end']) and sentiment_answer.sentiment == absa.Sentiment.negative:
                scoreDict[element] -= 1

    # Scale and return
    if scaleType == "linearScale":
        return linearScaleDict(scoreDict, 10, -10)
    elif scaleType == "cutOff":
        return cufOffScaleDict(scoreDict, 10, -10)
    elif scaleType == 'cutOffRound':
        return cufOffRoundScaleDict(scoreDict, 10, -10)


def countOccurencesScoreScaled_1_2(positive_answers, negative_answers, text, scaleType):

  # Create list with all indices of the string
  answerIndices = list(range(0, len(text)))

  # Counting number of occurences
  scoreDict = {}

  # Calculate positive scores
  for element in answerIndices:
    scoreDict[element] = 0
    for answer in positive_answers:
      if element in range(answer['start'], answer['end']):
        scoreDict[element] += 1*(1+answer['score'])

  for element in answerIndices:
    for answer in negative_answers:
      if element in range(answer['start'], answer['end']):
        scoreDict[element] -= 1*(1+answer['score'])

  # Scale and return
  if scaleType == "linearScale":
    return linearScaleDict(scoreDict, 10, -10)
  elif scaleType == "cutOff":
    return cufOffScaleDict(scoreDict, 10, -10)
  elif scaleType == 'cutOffRound':
    return cufOffRoundScaleDict(scoreDict, 10, -10)

def multipeQuestions(positiveAnswer, negativeAnswer, text, scaleType):

  # Combine results of one question type
  answerDicts = [countOccurences_1_1(positiveAnswer, negativeAnswer, text, scaleType) for positiveAnswer, negativeAnswer in zip(positiveAnswer, negativeAnswer)]

  # Creating one final dict
  return cutOffScaleDict(combineDicts(answerDicts), 10, -10)
