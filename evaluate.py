from QAABSA.DictEvaluation import countOccurences_1_1, countOccurenceswithABSA_1_1, countOccurencesScoreScaled_1_2, multipeQuestions
from QAABSA.htmlRenderer import renderOccurences
from QAABSA.extraction import getAspectSpans, isOverlapping
from QAABSA.utils import britishize, find_sub_list
import pandas as pd
from collections import Counter
import xml.etree.ElementTree as ET


# Imports for question creation
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from sklearn.metrics import f1_score
import spacy
nlp = spacy.load("en_core_web_lg")
stopwords = nlp.Defaults.stop_words
import string
nlp = English()
# Create a blank Tokenizer with just the English vocab
tokenizer = Tokenizer(nlp.vocab)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


class DataElement:

  def __init__(self, text, trueAspects, trueSpans, ignoreNeutral, asba_nlp):
    self.text = text
    self.textToken =
    self.length = len(text)
    self.evaluatedText = None

    self.trueAspects = trueAspects if not ignoreNeutral else [(text, senti) for (text, senti) in trueAspects if senti != 'neutral']
    self.trueSpans = trueAspects if not ignoreNeutral else [((int(x), int(y)), senti) for (x, y, senti) in trueSpans if senti != 'neutral']

    self.positivePredictions = None
    self.negativePredictions = None
    self.finalPredictionAspects = None
    self.finalPredictionSpans = None

    self.yTrue = None
    self.yPred = None

    self.nlp = asba_nlp


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


def generateResult(predictions, trues, text, tokenizer, stopwords):

  predictions = self.finalPredictionAspects
  trues = self.trueAspects
  text = self.text

  if type(predictions) is not list:
    predictions = [predictions]
  if type(trues) is not list:
    trues = [trues]

  tokenText = [token.text for token in list(tokenizer(text.translate(str.maketrans('', '', string.punctuation))))]

  y_pred = [0 for j in range(len(tokenText))]
  for prediction in predictions:
    predText, predSentiment = prediction
    tokenPred = [token.text for token in list(tokenizer(predText.translate(str.maketrans('', '', string.punctuation))))]

    for i in range(len(tokenText)):
      start, end =  find_sub_list(tokenPred, tokenText)
      if i >= start and i <= end:
        y_pred[i] = 1 if predSentiment == "positive" else -1

  y_true = [0 for j in range(len(tokenText))]
  for true in trues:
    trueText, trueSentiment = true
    tokenTrue = [token.text for token in list(tokenizer(trueText.translate(str.maketrans('', '', string.punctuation))))]

    for i in range(len(tokenText)):
      start, end =  find_sub_list(tokenTrue, tokenText)
      if i >= start and i <= end:
        y_true[i] = 1 if trueSentiment == "positive" else -1


  self.yTrue, self.yPred = y_true, y_pred



  def renderReview(self):
    renderOccurences(self.evaluatedText, self.text)


class ElementList:

  def __init__(self, ignoreNeutral, asba_nlp):
    self.dataElements = []
    self.length = len(self.dataElements)

    self.nlp = asba_nlp
    self.ignoreNeutral = ignoreNeutral

    self.yTrue = []
    self.yPred = []


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

  def binaryEval(self):
      for dataElement in self.dataElements:
          self.binaryTrue.append(dataElement.binaryTrue)
          self.binaryPred.append(dataElement.binaryPred)




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
