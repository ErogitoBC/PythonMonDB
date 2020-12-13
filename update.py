import json
from bson import json_util
from bson.json_util import dumps
from pymongo import MongoClient
connection = MongoClient('localhost', 27017)
database = connection['market']
collection = database['stocks']

def updateDocument(query,update):
  try:
    line = "--" * 50  
    collection.update_many(query,update)
    result=collection.find(query,{"Current Ratio":1,"Ticker":1,"Total Debt/Equity":1,"Volume":1}).limit(10)
    print("\t\t Results");
    print("--" * 50)
    print(dumps(result))
    print(line+"\n\n")
  except ValidationError as ve:
    abort(400, str(ve))
  

def main():
  line = "--" * 45  
  print(line+"\n\n")
  print("\t\t Provide The Ticker Value for The Documents To Be Updated. \n");
  print(line+"\n")
  tvalue = raw_input("Enter Ticker Value# ")
  print("Received >>"+tvalue);
  print(">> Ticker Values displayed Below.");
  query = {"Ticker" : tvalue}
  result=collection.find(query,{"Current Ratio":1,"Ticker":1,"Total Debt/Equity":1,"Volume":1}).limit(10)
  print(dumps(result))
  
  print(line+"\n")
  
  
  print("Change the Volume. \n")
  volume = float(raw_input("New Volume#"))
  
  print("Request being processed. ")
  print(line+"\n")
  
  
  update =  { "$set":{"Volume":volume}}
  updateDocument(query,update)
  
main()