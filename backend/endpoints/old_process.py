'''
@app.post("/api/process-audio")
async def process_audio(audio: UploadFile = File(...)):
    try:
        # Dynamically create a temporary folder for audio files
        TEMP_FOLDER = Path("temp_audio")
        TEMP_FOLDER.mkdir(exist_ok=True)

        # Save the audio file temporarily
        temp_audio_path = TEMP_FOLDER / audio.filename
        with temp_audio_path.open("wb") as temp_file:
            shutil.copyfileobj(audio.file, temp_file)

            print("1 - WORKS")

        # Forward audio to Vosk for transcription
        with temp_audio_path.open("rb") as audio_file:
            files = {"audio": (audio.filename, audio_file, audio.content_type)}
            vosk_response = requests.post("http://localhost:2700/transcript", files=files)

        if vosk_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to process audio with Vosk.")
        print("2 - WORKS")

        vosk_data = vosk_response.json()
        transcription = vosk_data.get("text", "")
        accuracy = vosk_data.get("confidence", 0.0)

        print(vosk_data)
        print(transcription)
        print(accuracy)

        # Gemini API interaction
        gemini_headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}

        # First payload: Grammar improvement tips
        grammar_payload = {
            "input": f"{transcription}\n\nTell me how I can improve my grammar based on my confidence score of {accuracy}."
        }
        grammar_response = requests.post(
            "https://api.gemini.com/v1/converse",
            json=grammar_payload,
            headers=gemini_headers,
        )
        if grammar_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to process transcript with Gemini (grammar tips).")
        grammar_tips = grammar_response.json()

        # Second payload: Autogenerate a new question
        question_payload = {"input": f"{transcription}\n\nGenerate a follow-up question based on the user's input."}
        question_response = requests.post(
            "https://api.gemini.com/v1/converse",
            json=question_payload,
            headers=gemini_headers,
        )
        if question_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to process transcript with Gemini (new question).")
        new_question = question_response.json()

        # Format the data into a schema before inserting into MongoDB
        document = {
            "audio_file": audio.filename,
            "transcription": transcription,
            "accuracy": accuracy,
            "gemini": {
                "grammar_tips": grammar_tips,
                "new_question": new_question,
            },
        }

        # Insert the formatted document into the single collection
        collection.insert_one(document)

        # Send the new question to the frontend
        return {"new_question": new_question}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up the temporary file
        if temp_audio_path.exists():
            temp_audio_path.unlink()
        # Remove the temp folder if empty
        if TEMP_FOLDER.exists() and not any(TEMP_FOLDER.iterdir()):
            TEMP_FOLDER.rmdir()
'''

