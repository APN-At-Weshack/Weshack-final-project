from fastapi import FastAPI, HTTPException
from fastapi import APIRouter
from pymongo import MongoClient
from dotenv import load_dotenv
import google.generativeai as genai
import os
import uuid

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")  # Default collection name

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=GEMINI_API_KEY)

# FastAPI setup
app = APIRouter()

@app.get("/")
def ask_gemini():
    """
    API endpoint to ask Gemini a random question for the user to answer in a given language.
    Saves the question to MongoDB and returns the MongoDB document ID and the question.
    """

    # Prompt for Gemini
    prompt = f"Hello Gemini, I'm learning English. Can you ask me an easy and random question to test how well I'm able to speak and answer in that language?"

    # Generate response using the google-generativeai library
    try:
        response = model.generate_content(prompt)

        # Create an object to store in MongoDB
        question_object = {
            "question number": 0,  
            "language": "English",
            "question": response.text,
            "conId": uuid.uuid4().hex
        }

        # Insert the object into MongoDB
        result = collection.insert_one(question_object)
        object_id = question_object["conId"]
        
        # Return the response
        return {"id": str(object_id), "question": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate a question: {str(e)}")
