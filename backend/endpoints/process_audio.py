from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi import APIRouter
from pymongo import MongoClient
from bson import ObjectId
import requests
import os
import shutil
from dotenv import load_dotenv
from pathlib import Path
import google.generativeai as genai
app = APIRouter()

load_dotenv()

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DATABASE_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=GEMINI_API_KEY)


@app.post("/")
async def process_audio(audio: UploadFile = File(...), conID: str = Form(...)):
    try:
            print(conID)
            # Create a temporary folder for audio files
            TEMP_FOLDER = Path("temp_audio")
            TEMP_FOLDER.mkdir(exist_ok=True)

            # Ensure the filename ends with .wav
            filename_with_extension = audio.filename
            if not filename_with_extension.endswith(".wav"):
                filename_with_extension += ".wav"

            # Save the audio file temporarily with the .wav extension
            temp_audio_path = TEMP_FOLDER / filename_with_extension
            with temp_audio_path.open("wb") as temp_file:
                shutil.copyfileobj(audio.file, temp_file)

            # Read the audio file into memory
            with temp_audio_path.open("rb") as audio_file:
                audio_data = audio_file.read()

            # Create the headers and options to send the request
            vosk_url = "http://localhost:2700/transcript"  # Change to your Vosk URL
            headers = {
                "Accept": "application/json",
                "Content-Type": "audio/wav",
            }

            # Send the request with the audio file data
            responses = requests.post(vosk_url, headers=headers, data=audio_data)

            if responses.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to process audio with Vosk.")

            vosk_data = responses.json()

            confidence_numbers = [entry['conf'] for entry in vosk_data['vosk']['result']]
            average_confidence = sum(confidence_numbers) / len(confidence_numbers) if confidence_numbers else 0



            #Promt 1 output and formatting
            prompt = f"{vosk_data}\n\nTell me how I can improve my grammar based on my confidence score of {vosk_data}, and check the grammar to show where I tend to mess up. Limit the response to be short and simple, nothing too long."
            response = model.generate_content(prompt)
            #object_id = result.inserted_id
            # p1data = json.loads(response.text)
            # p1data["response"] = p1data["response"].replace('\n', '')
            
            #Promt 2 question
            prompt2 = f"{vosk_data}\n\nPlease ask me another question based off my answer that relates to me learning english, please try to make the vocabulary as simple as possible and avoid using complex words. Don't ask me unrelated questions related that don't involve me answering in a way to learn english thank you. ONLY repond with a new question and do not comment on my performance of the previous sentence"
            response2 = model.generate_content(prompt2)

            print(response2)
            question_object = {
                "question response": response.text,
                "question asked": response2.text,
                "vosk data": vosk_data
            }
            
            collection.update_one(
                {"conID": conID},  # Match the document with the provided ObjectID (conID)
                {
                    "$setOnInsert": {"conID": conID},  # Only set if a new document is created
                    "$push": {  # Append to an array if applicable
                        "History": question_object  # Add question_object to the History array
                    }
                },
                upsert=True  # Create a new document if no match is found
            )            

            result_object = {
                "Response": response.text,
                "Question": response2.text,
                "ConfidenceScore": average_confidence * 100
            }

            return(result_object)
      
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up the temporary file
        if temp_audio_path.exists():
            temp_audio_path.unlink()
        # Remove the temp folder if empty
        if TEMP_FOLDER.exists() and not any(TEMP_FOLDER.iterdir()):
            TEMP_FOLDER.rmdir()
