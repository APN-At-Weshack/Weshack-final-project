from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from fastapi import APIRouter
import requests
import os
import shutil
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

app = APIRouter()

@app.get("/")
async def get_sample_data():
    """Returns sample JSON data."""
    return {
        "message": "Welcome to the English Helping Tool API!",
        "examples": {
            "upload_audio": {
                "method": "POST",
                "endpoint": "/process-audio",
                "description": "Send a .wav audio file for processing",
            },
            "get_sample_data": {
                "method": "GET",
                "endpoint": "/sample-data",
                "description": "Returns sample JSON data",
            },
        },
    }