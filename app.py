
print("import Library...")
import numpy as np, hazm, pandas as pd,sys , collections,math
from hazm import *
import codecs
import xml.etree.ElementTree as ET
from bplustree import BPlusTree

class Item:
  def __init__(self):
    self.text = ''
    self.date = ''
    self.cat = ''
    self.titel = ''
    self.id = ''

print("Loading XML...")
MyData = []
tree = ET.parse('data.xml')
root = tree.getroot()
id = 0
for child in root: # DOC
    myItem = Item()
    for child1 in child:  
        if child1.tag == "TEXT":
            myItem.text = child1.text
        if child1.tag == "ISSUE":
            myItem.date = child1.text
        if child1.tag == "TITLE":
            myItem.titel = child1.text
        if child1.tag == "CAT":
            myItem.cat = child1.text
        if child1.tag == "DOCID":
            #myItem.id = child1.text
            myItem.id = id
            id+=1
    MyData.append(myItem)

print("Loading Stope Words...")
rlist = codecs.open("Removable charecters.txt", encoding='utf-8').read().split('\n')
removeable = [c[0] for c in rlist]
nmz = Normalizer()
wordTokenizer = WordTokenizer()
lemmatizer = Lemmatizer()
slist = codecs.open('Stops.txt', encoding='utf-8').read().split('\n')
stops = sorted(list([nmz.normalize(w) for w in slist if w]))

print("Processing data...")
def Process(TEXT):        
    TEXT = ''.join([c for c in TEXT if c not in removeable])
    TEXT = nmz.character_refinement(TEXT) # pack kardan kalamat arabi va adad englisi
    TEXT = nmz.affix_spacing(TEXT) # tabdile fasele be nim fasele                 
    tokens = wordTokenizer.tokenize(TEXT)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stops]                     
    tokens = set(tokens)
    tokens = sorted(list(tokens))        
    return tokens

class TokenItem:
  def __init__(self):
    self.DocId = ''
    self.Tokens = []

TokenList = []

for item in MyData:
    t = TokenItem()
    t.DocId = item.id
    t.Tokens = Process(item.text)
    TokenList.append(t)

print("Creating posting...")
Posting = {}
def addDoc(token,docID):
    global Posting
    if(token not in Posting):
        Posting[token] = []
    Posting[token].append(docID)                               
    
def Assignment(tokenitem): 
    pd.Series(tokenitem.Tokens).apply(lambda token: addDoc(token, tokenitem.DocId));        


for i in TokenList:
    Assignment(i)

for v in Posting.values():
    v = sorted(v)


def Query(Text):
    try:
        WordTokens = Process(Text)
        posting_List = []
        for word in WordTokens:
            posting = Posting[word]
            posting_List.append(posting)

        if(len(posting_List) == 0):
            return []

        FInalPosting = posting_List[0]

        for plist in posting_List:
            FInalPosting = set(FInalPosting).intersection(plist)
            
        return sorted(FInalPosting)        
    except:
        return []

def GetDocList(Text):
    posintg = Query(Text)
    DocList = []
    for docId in posintg:
        for item in MyData:
            if(docId == item.id):
                jData = {
                    'Id' : item.id,
                    'Category' : item.cat,
                    'Titel' : item.titel,
                    'Text' : item.text[0:20] + " ...",
                    'Date' : item.date
                }
                DocList.append(jData)
    return DocList

def GetDoc(DocId):
    intId = int(DocId)
    for item in MyData:
        if(item.id == intId):
            return {
                'Id' : item.id,
                'Category' : item.cat,
                'Titel' : item.titel,
                'Text' : item.text,
                'Date' : item.date
            }
    return {
            'Id' : DocId,
            'Category' : '',
            'Titel' : '',
            'Text' : '',
            'Date' : ''
        }

def GetSuggestion(Text):
    w = Text.split(' ')
    last = w[len(w)-1]
    index = Text.index(last)
    #res = forward.find(last).values
    res = []
    for i in Posting.keys():
        if(i.startswith(last)):
            res.append(Text[0:index] + i)
    return res