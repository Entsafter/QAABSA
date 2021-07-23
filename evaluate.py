from QAABSA.DictEvaluation import countOccurences_1_1, countOccurenceswithABSA_1_1, countOccurencesScoreScaled_1_2
from QAABSA.htmlRenderer import renderOccurences
from QAABSA.extraction import getAspectSpans
import pandas as pd
import xml.etree.ElementTree as ET


class DataElement:

  def __init__(self, text, trueAspects, trueSpans, asba_nlp):
    self.text = text
    self.length = len(text)
    self.evaluatedText = None

    self.trueAspects = trueAspects
    self.trueSpans = trueSpans

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

  def addPredictions(self, positivePredictions, negativePredictions, evalType, spanType):
    self.positivePredictions = positivePredictions
    self.negativePredictions = negativePredictions

    if evalType == 'countOccurenceswithABSA_1_1':
      self.evaluatedText = countOccurenceswithABSA_1_1(positivePredictions, negativePredictions, self.text, "cutOff", nlp_sentiment=self.nlp)
    elif evalType == 'countOccurences_1_1':
      self.evaluatedText = countOccurences_1_1(positivePredictions, negativePredictions, self.text, "cutOff", nlp_sentiment=self.nlp)
    elif evalType == 'countOccurencesScoreScaled_1_2':
       self.evaluatedText = countOccurences_1_1(positivePredictions, negativePredictions, self.text, "cutOff", nlp_sentiment=self.nlp)

    self.finalPredictionSpans, self.finalPredictionAspects = getAspectSpans(self.evaluatedText, self.text, type=spanType)


  def evaluatePrediction(self, predType):
    # Checking if the aspect is in the prediction
    # This can only be used if the trueAspect is very short
    if predType == "inside":
      self.TP = len([trueAspect for trueAspect in self.trueAspects if any(trueAspect in predAspect for predAspect in self.finalPredictionAspects)])
      self.FN = len([trueAspect for trueAspect in self.trueAspects if not any(trueAspect in predAspect for predAspect in self.finalPredictionAspects)])
      self.FP = len([predAspect for predAspect in self.finalPredictionAspects if not any(true in predAspect for true in self.trueAspects)])
    elif predType == "overlap":
      self.TP = len([trueSpan for trueSpan in self.trueSpans if any(isOverlapping(trueSpan, predSpan) for predSpan in self.finalPredictionSpans)])
      self.FN = len([trueSpan for trueSpan in self.trueSpans if not any(isOverlapping(trueSpan, predSpan) for predSpan in self.finalPredictionSpans)])
      self.FP = len([predSpan for predSpan in self.finalPredictionSpans if not any(isOverlapping(trueSpan, predSpan) for trueSpan in self.trueSpans)])

    self.F1 = self.TP/(self.TP+0.5*(self.FP+self.FN))

  def renderReview(self):
    renderOccurences(self.evaluatedText, self.text)


class ElementList:

  def __init__(self, asba_nlp):
    self.dataElements = []
    self.length = len(self.dataElements)

    self.nlp = asba_nlp

    self.TP = 0
    self.TN = 0
    self.FP = 0
    self.FN = 0
    self.F1 = 0

  def inputFile(self, path, fileType):
    if fileType == 'Laptop':
      df = self.readLaptop(path)

    for index, row in df.iterrows():
      dE = DataElement(row['text'], row['aspects'], row['spans'], asba_nlp=self.nlp)


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