import json
from bson import json_util
from bson.json_util import dumps
from pymongo import MongoClient
connection = MongoClient('localhost', 27017)
database = connection['market']
collection = database['stocks']

def deleteDocument(document,tvalue):
  try:
    line = "--" * 45  
    print(line)
    result = collection.remove(document)
    print("----------Documents With Ticker Value "+tvalue+" Have Been Deleted  \n")
    print(dumps(result))
  except ValidationError as ve:
    abort(400, str(ve))
  

def main():
  line = "--" * 45  
  print(line+"\n\n")
  print("\t\t !!WARNING!! !!Document(s) Associated with Ticker Value will be Deleted!\n");
  print(line+"\n")
  tvalue = raw_input("Enter Ticker Value #")
  
  myquery = {"Ticker" : tvalue}
  
  print("--" * 50 +" Items Below Will Be Deleted " + "--"*50+" \n")
  result=collection.find(myquery).limit(10)
  print(dumps(result))
  deleteDocument(myquery,tvalue)
main()