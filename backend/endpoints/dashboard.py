from fastapi import FastAPI, HTTPException
from fastapi import APIRouter
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util
import json
import os

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")  # Default collection name

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# FastAPI setup
app = APIRouter()

@app.get("/")
def get_history():
    """
    Query MongoDB for all documents and extract unique conIds.
    """
    try:
        # Query all documents from the collection
        documents = collection.find()
        
        # Convert the documents to a JSON-serializable format
        json_docs = json.loads(json_util.dumps(documents))
        
        return json_docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
