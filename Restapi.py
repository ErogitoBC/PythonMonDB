#!/usr/bin/python
import json
from bson import json_util
from bson.json_util import dumps
import bottle
from bottle import route, run, request, abort
from pymongo import MongoClient
connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

@route('/update/<TickerValue>', method='PUT')
def UpdateMyStock(TickerValue):
  jsondata = request.json 
  query = { "Ticker" : TickerValue} 
 
  
  for key in jsondata:
    update =  { "$set":{key:jsondata[key]}}
    collection.update(query,update)
  updateDocs = collection.find({"Ticker":TickerValue})
  line = "--" * 45 +"\n" 
  result = dumps(updateDocs) 
  return line+"\n   Updated Document>>  \n"+str(result) +line

   
  
@route('/addDoc', method='POST')
def addDocumentStock():
  jsonData = request.json
  newDocument = collection.insert(jsonData)
  retriveDoc = collection.find_one({"_id":newDocument})
  line = "--" * 45 +"\n"
  return line+ "\nAdded Document >> \n "+dumps(retriveDoc)+"\n End Of Document >>\n "+line #return inserted document.

@route('/addDoc/<tickerValue>', method='POST')
def addDocumentStock(tickerValue):
  jsonData = request.json
  jsonData.update( {'Ticker' : tickerValue} ) 
  recordId = collection.insert(jsonData)
  retriveDoc = collection.find_one({"_id":recordId})
  line = "--" * 45 +"\n"
  return line+ "\nAdded Document>> \n "+dumps(retriveDoc) +line 


@route('/remove/<TickerValue>', method='GET')
def removeStock(TickerValue):
  query = {"Ticker" :TickerValue} 
  result = collection.delete_many(query) 
  return "\n Requested Document in the Collection has been deleted.  \n" 

@route('/RequestDoc/<TickerValue>', method='GET')
def requestDocument(TickerValue):
  readDocument = collection.find({"Ticker":TickerValue}) 
  #provided
  line = "--" * 45 +"\n"
  return line+"\n Requested Document >>\n "+dumps(readDocument)+" \n End Of Requested Document >>"

@route('/RequestDoc/', method='GET')
def requestDocument():
  readDocument = collection.find().limit(1) 
  line = "--" * 45 +"\n"
  return line+"\n Requested Document >>\n "+dumps(readDocument)+" \n End Of Requested Document >>\n"

@route('/stockSummery/', method='POST')
def getReport(): 
  line = "--" * 45 +"\n"
  tickerSymbols = request.json.get('list') 
  tickerSymbols = tickerSymbols.replace("[","")
  tickerSymbols = tickerSymbols.replace("]","")
  tickerSymbols = list(tickerSymbols.split(",")) 
  EmptyTickers = list()
  print(tickerSymbols)
  underline = "_" * 30;
 
  for ticker in tickerSymbols:
      item = Pipeline(ticker)
      print(item)
      
      EmptyTickers.append(line+" \t\t\t **Report For Value ["+ticker+"] ** \n \t\t\t"+underline+" \n"+item+"\n\n "+line)
  return EmptyTickers 


@route('/getIndustryReport/<industryName>', method='GET')
def getReport(industryName):
  industry = industryName.replace("+"," ")
  print("\n\n\n "+industry+"\n\n")
  result2 = IndustryPipeline(industry)
  firstStage = { '$project': {'Industry':1, 'Ticker':1,'Float Short':1,'Relative Volume':1,'Volume':1,'Performance (Year)':1 } }
  secondStage = { '$match': { "Industry": industry } }
  print("\n\n\n "+str(secondStage)+"\n\n")
  thirsStage = { '$group': { '_id': "$Industry", 'Total Float Short': {'$sum': "$Float Short" },
                           'Average Relative Volume':{'$avg':"$Relative Volume"},
                           'Average Volume':{'$avg':'$Volume'},
                           'Max Performance (Year)':{'$max':'$Performance (Year)'},
                           'Total Volume':{'$sum':'$Volume'} } }
  
  fourthStage = { '$limit' : 5 }
  query = [firstStage,secondStage,thirsStage,fourthStage]
  print(str(query))
  result=collection.aggregate(query)
  result = dumps(result)
  return "-------- \n \t\t\t Portfolio Report For  ["+industry+"] Industrie(s) \n\n "+result+" \n-------- \n"+result2+"\n"

def Pipeline(ticker):

  firstStage = { '$project': { 'Ticker':1,'Float Short':1,'Relative Volume':1,'Volume':1,'Performance (Year)':1 } }

  secondStage = { '$match': { "Ticker": ticker } }

  thirdStage = { '$group': { '_id': "$Ticker", 'Total Float Short': {'$sum': "$Float Short" },
                           'Average Relative Volume':{'$avg':"$Relative Volume"},
                           'Total Accupied Volume':{'$sum':'$Volume'},
                           'Max Performance (Year)':{'$max':'$Performance (Year)'},
                           'Minimum Volume Used':{'$min':'$Volume'} } }
  myQuery = [firstStage,secondStage,thirdStage]
  result=collection.aggregate(myQuery) 
  result = dumps(result)
  return result



def IndustryPipeline(industry):
  
  firstStage = { '$project': { 'Industry':1,'Float Short':1,'Price':1,'Average True Range':1,'50-Day Simple Moving Average':1,'Change':1 } }

  secondStage = { '$match': { "Industry": industry } }

  thirdStage = { '$group': { '_id': "$Industry", 'Total Float Short': {'$sum': "$Float Short" },
                           'Average Average True Range':{'$avg':"$Average True Range"},
                           'Total Price':{'$sum':'$Price'},
                           'Max 50-Day Simple Moving Average (Year)':{'$max':'$50-Day Simple Moving Average'},
                           'Minimum Change':{'$min':'$Change'} } }

  fourthStage = { '$limit' : 5 }
  myQuery = [firstStage,secondStage,thirdStage,fourthStage]
  result=collection.aggregate(myQuery) 
  result = dumps(result)
  return "-------- \n Stock Information \n\n"+result+"\n\n"


if __name__ == '__main__':
  run(debug=True,reloader = True)
  #run(host='localhost', port=8080)
  