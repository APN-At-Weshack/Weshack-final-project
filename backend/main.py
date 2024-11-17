# from fastapi import FastAPI
# from endpoints.test import app as test_router
# from endpoints.first_question import app as first_question_router
# from endpoints.process_audio import app as process_audio_router

# app = FastAPI()

# # Include the routers with appropriate prefixes
# app.include_router(test_router, prefix="/api/test", tags=["Test"])
# app.include_router(first_question_router, prefix="/api/ask-gemini", tags=["Ask Gemini"])
# app.include_router(process_audio_router, prefix="/api/process-audio2", tags=["Process Audio"])

# # Root endpoint
# @app.get("/")
# def root():
#     return {"message": "Welcome to the English Learning API!"}

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from endpoints.test import app as test_router
from endpoints.first_question import app as first_question_router
from endpoints.process_audio import app as process_audio_router
from endpoints.dashboard import app as dashboard_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers with appropriate prefixes
app.include_router(test_router, prefix="/api/test", tags=["Test"])
app.include_router(first_question_router, prefix="/api/ask-gemini", tags=["Ask Gemini"])
app.include_router(process_audio_router, prefix="/api/process-audio2", tags=["Process Audio"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["History"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the English Learning API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=4000)