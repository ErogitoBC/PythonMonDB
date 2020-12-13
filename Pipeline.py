import json
from bson import json_util
from bson.json_util import dumps
from pymongo import MongoClient
connection = MongoClient('localhost', 27017)
database = connection['market']
collection = database['stocks']

def pipeline(pipe):
  try:
    line = "--" * 45  
    print(line+"\n")
    result=collection.aggregate(pipe)
    result = dumps(result)
    print(result)
    print(line+"\n")
  except ValidationError as ve:
    abort(400, str(ve))
  

def main():
  line = "--" * 45  
  print("\t\t Please Enter Sector Name Down Below\n");
  print(line+"\n")
  sectorname = raw_input("Name Of The Sector: ")
  Match = { '$match': { "Sector": sectorname } }
  group = { '$group': { '_id': "$Industry", 'Total Outstanding Shares:': {'$sum': "$Shares Outstanding" } } }
  pipe = [Match, group]
  pipeline(pipe)
main()