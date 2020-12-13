import json
from bson import json_util
from pymongo import MongoClient
connection = MongoClient('localhost', 27017)
database = connection['market']
collection = database['stocks']

def insertDocument(document):
  message = ""
  try:
    result=collection.insert(document)
    message = "Document Added"
  except ValidationError as ve:
    abort(400, str(ve))
  return message

def main():
  line = "--" * 45  
  print(line+"\n\n")
  document = raw_input("Enter Your Document:")
  print("Document Processed \n"+line)
  print(document)
  print insertDocument(json.loads(document))
  print(line+"\n\n")
  
main()