import json
from bson import json_util
from bson.json_util import dumps
from pymongo import MongoClient
connection = MongoClient('localhost', 27017)
database = connection['market']
collection = database['stocks']

def findDocument(query,toDisplay):
  try:
    line = "--" * 45 
    print(line+"\n")
    result=collection.find(query,toDisplay)
    print(dumps(result))
    print(line+"\n")
  except ValidationError as ve:
    abort(400, str(ve))
  

def main():
  line = "--" * 45  
  print("\t\t Enter The Name Of The Industry Down Below \n");
  print(line+"\n")
  industryname = raw_input("Name Of The Industry: ")
  query = {"Industry" : industryname}
  toDisplay = {"Ticker":1,"_id":0}
  findDocument(query,toDisplay)
 
main()
