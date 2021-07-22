from IPython.core.display import display, HTML

def renderOccurences(countDict, text):

  # Takes a dict with keys representing the position of the letter,
  # values representing the relative sentiment of the letter
  # -10 <= x <= 10
  # -10 -> max negative
  # 10 max positive

  # Create colour gradient
  COLOURS =  {-1:"#fdedec",
               -2:"#fde9e8",
               -3:"#fad4d1",
               -4:"#f8beba",
               -5:"#f5a8a3",
               -6:"#f3928c",
               -7:"#f07d75",
               -8:"#ee675d",
               -9:"#ec5146",
               -10:"#e93c2f",
                0:"#ffffff",
                1:"#edf8f6",
                2:"#daf1ec",
                3:"#c8eae3",
                4:"#b6e2d9",
                5:"#a3dbd0",
                6:"#91d4c7",
                7:"#7ecdbd",
                8:"#6cc6b4",
                9:"#5abfab",
               10:"#45b39d"}


  # Combine areas with same colour
  i = 0
  outputDict = {}
  lastElement = None
  start = None
  end = None
  while i in range(len(countDict)):
    if lastElement == None:
      start = i
      lastElement = countDict[i]

    if lastElement != countDict[i]:
      outputDict[(start, i-1)] = countDict[i-1]
      start = i
      lastElement = countDict[i]

    if i + 1 == len(countDict):
      outputDict[(start, i)] = countDict[i]
    i += 1


  # Convert count -> colour
  position_html = {}
  for position, count in outputDict.items():
    position_html[position] = COLOURS[count]

  # Convert colour -> html
  html_text = ""
  for element in position_html.items():
    span, colour = element
    start, end = span
    html_text += f'<span style="background-color:{colour}">' + text[start:end+1] + '</span>'

  # Create and display HTML
  HTML_HEAD = '<head> <style>body{font-family: "proxima-soft", "Proxima Soft", "Proxima Nova Soft", "Helvetica, Arial", sans-serif;}span{background-color: gray; padding-top:5px; padding-bottom:5px; line-height: 2.2em; font-weight: bold; border-radius: 5px 5px; -webkit-box-decoration-break: clone; -o-box-decoration-break: clone; box-decoration-break: clone;}p{background-color: #EBEDEF; padding: 5px; font-family: "proxima-soft", "Proxima Soft", "Proxima Nova Soft", "Helvetica, Arial", sans-serif; font-weight: bold; border-radius: 5px 5px;}.background{background-color:#EBEDEF; padding:10px; padding-left:3px; padding-right:4px; -webkit-box-decoration-break: clone; -o-box-decoration-break: clone; box-decoration-break: clone;}</style></head>'
  HTML_BODY = f'<body><span class="background">{html_text}</span><br><br></body>'
  display(HTML(HTML_HEAD + HTML_BODY))
