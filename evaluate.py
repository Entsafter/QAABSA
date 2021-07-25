from QAABSA.DictEvaluation import countOccurences_1_1, countOccurenceswithABSA_1_1, countOccurencesScoreScaled_1_2, multipeQuestions
from QAABSA.htmlRenderer import renderOccurences
from QAABSA.extraction import getAspectSpans, isOverlapping
from QAABSA.utils import britishize
import pandas as pd
from collections import Counter
import xml.etree.ElementTree as ET

# Imports for question creation
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


class DataElement:

  def __init__(self, text, trueAspects, trueSpans, ignoreNeutral, asba_nlp):
    self.text = text
    self.length = len(text)
    self.evaluatedText = None

    self.trueAspects = trueAspects if not ignoreNeutral else [(text, senti) for (text, senti) in trueAspects if senti != 'neutral']
    self.trueSpans = trueAspects if not ignoreNeutral else [((int(x), int(y)), senti) for (x, y, senti) in trueSpans if senti != 'neutral']

    self.positivePredictions = None
    self.negativePredictions = None
    self.finalPredictionAspects = None
    self.finalPredictionSpans = None

    self.nlp = asba_nlp

    self.TP = 0
    self.TN = 0
    self.FP = 0
    self.FN = 0
    self.F1 = 0

  def addPredictions(self, positivePredictions, negativePredictions, evalType, spanType, maxScore, excludePercentage):
    self.positivePredictions = positivePredictions
    self.negativePredictions = negativePredictions

    if evalType == 'countOccurenceswithABSA_1_1':
      self.evaluatedText = countOccurenceswithABSA_1_1(positivePredictions, negativePredictions, self.text, "cutOff", nlp_sentiment=self.nlp)
    elif evalType == 'countOccurences_1_1':
      self.evaluatedText = countOccurences_1_1(positivePredictions, negativePredictions, self.text, "cutOff")
    elif evalType == 'countOccurencesScoreScaled_1_2':
       self.evaluatedText = countOccurencesScoreScaled_1_2(positivePredictions, negativePredictions, self.text, "cutOff")

    elif evalType == 'multipleQuestions':
       self.evaluatedText = multipeQuestions(positivePredictions, negativePredictions, self.text, "cutOff")

    self.finalPredictionSpans, self.finalPredictionAspects = getAspectSpans(self.evaluatedText, self.text, maxScore, excludePercentage, type=spanType)


  def evaluatePrediction(self, predType, ElementList):
    # Checking if the aspect is in the prediction
    # This can only be used if the trueAspect is very short
    if predType == "inside":
      self.TP = len([trueAspect for trueAspect in self.trueAspects if any(trueAspect in predAspect for predAspect in self.finalPredictionAspects)])
      self.TN = 1 if not (self.trueSpans and self.finalPredictionSpans) else 0
      self.FN = len([trueAspect for trueAspect in self.trueAspects if not any(trueAspect in predAspect for predAspect in self.finalPredictionAspects)])
      self.FP = len([predAspect for predAspect in self.finalPredictionAspects if not any(true in predAspect for true in self.trueAspects)])
    elif predType == "overlap":
      self.TP = len([trueSpan for trueSpan, trueSenti in self.trueSpans if any(isOverlapping(trueSpan, predSpan) and trueSenti == predSenti for predSpan, predSenti, predScore in self.finalPredictionSpans)])
      self.TN = 1 if not (self.trueSpans and self.finalPredictionSpans) else 0
      self.FN = len([trueSpan for trueSpan, trueSenti in self.trueSpans if not any(isOverlapping(trueSpan, predSpan) and trueSenti == predSenti for predSpan, predSenti, predScore in self.finalPredictionSpans)])
      self.FP = len([predSpan for predSpan, predSenti, predScore in self.finalPredictionSpans if not any(isOverlapping(trueSpan, predSpan) and trueSenti == predSenti for trueSpan, trueSenti in self.trueSpans)])

    elif predType == 'overall':
      self.TP = len([trueSpan for trueSpan, trueSenti in self.trueSpans if any(isOverlapping(trueSpan, predSpan) and trueSenti == predSenti for predSpan, predSenti, predScore in self.finalPredictionSpans)])
      self.TN = 1 if not (self.trueSpans and self.finalPredictionSpans) else 0
      self.FN = len([trueSpan for trueSpan, trueSenti in self.trueSpans if not any(isOverlapping(trueSpan, predSpan) and trueSenti == predSenti for predSpan, predSenti, predScore in self.finalPredictionSpans)])
      self.FP = len([predSpan for predSpan, predSenti, predScore in self.finalPredictionSpans if not any(isOverlapping(trueSpan, predSpan) and trueSenti == predSenti for trueSpan, trueSenti in self.trueSpans)])
      self.TP = 1 if not (self.FP or self.FN) else 0
      self.TN = 1 if not (self.trueSpans and self.finalPredictionSpans) else 0
      self.FN = 1 if self.FN else 0
      self.FP = 1 if self.FP else 0


    if not (self.TP == 0 and self.FN == 0 and self.FP == 0):
        self.F1 = self.TP/(self.TP+0.5*(self.FP+self.FN))
    else:
        self.TP = 1
        self.F1 = 1



  def renderReview(self):
    renderOccurences(self.evaluatedText, self.text)


class ElementList:

  def __init__(self, ignoreNeutral, asba_nlp):
    self.dataElements = []
    self.length = len(self.dataElements)

    self.nlp = asba_nlp
    self.ignoreNeutral = ignoreNeutral

    self.TP = 0
    self.TN = 0
    self.FP = 0
    self.FN = 0
    self.F1 = 0

  def generateQuestions(self, k):

    reviews = ""
    for dataElement in self.dataElements:
        reviews += dataElement.text

    lem = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(reviews)
    word_tokens = [word for (word, tag) in nltk.pos_tag(word_tokens) if tag == "NN"]

    counterDict = Counter([britishize(lem.lemmatize(w)) for w in word_tokens if not w.lower() in list(stop_words) + [',', '.', '?', '!', '-']])
    mostCommonWords = [k for k, v in counterDict.most_common(k)]

    positiveQuestions = []
    negativeQuestions = []
    for aspect in mostCommonWords:
        positiveQuestions.append(f"What is amazing about the {aspect}?")
        negativeQuestions.append(f"What is terrible about the {aspect}?")

    return positiveQuestions, negativeQuestions




  def inputFile(self, path, fileType):
    if fileType == 'Laptop':
      df = self.readLaptop(path)

    for index, row in df.iterrows():
      dE = DataElement(row['text'], row['aspects'], row['spans'], ignoreNeutral=self.ignoreNeutral, asba_nlp=self.nlp)
      self.dataElements.append(dE)
      self.length = len(self.dataElements)

  def addScores(self, TP, TN, FP, FN):
      self.TP += TP
      self.TN += TN
      self.FP += FP
      self.FN += FN

      self.F1 = self.TP/(self.TP+0.5*(self.FP+self.FN))




  def readLaptop(self, path):
    tree = ET.parse(path)
    root = tree.getroot()

    df_Laptop = pd.DataFrame({'text':[], 'aspects':[], 'spans':[]}, index=[])

    for sentence in root:
      for child in sentence.iter("text"):
        text = child.text

      aspects = []
      spans = []
      for child in sentence.iter("aspectTerm"):
        spans.append((child.attrib['from'], child.attrib['to'], child.attrib['polarity']))
        aspects.append((child.attrib["term"], child.attrib['polarity']))

      df_Laptop = df_Laptop.append({'text':text,'aspects':aspects, 'spans':spans}, ignore_index=True)

    return df_Laptop
