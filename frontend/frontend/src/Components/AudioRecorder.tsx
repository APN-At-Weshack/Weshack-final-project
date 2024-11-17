"use client"
// components/AudioRecorder.tsx
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

import RecordRTC, { RecordRTCPromisesHandler, StereoAudioRecorder } from 'recordrtc';

interface AudioRecorderProps {
  conID: string;
  question: string;
}

export default function AudioRecorder(props: AudioRecorderProps) {
  const [recorder, setRecorder] = useState<RecordRTCPromisesHandler | null>(null);
  const audioChunks = useRef<Blob[]>([]);
  const [geminiResponse, setGeminiResponse] = useState<string>(""); // Initialize response state
  const [firstRec, setFirstRec] = useState<boolean>(true);
  const [conversations, setConversations] = useState([
    {
      aiQuestion: props.question,
      Response: '',
      ConfidenceScore: '',
      Question: '',
    },
  ]);

  // Function to get permission and initialize recorder
  const getPermissionInitializeRecorder = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      const recorderInstance = new RecordRTCPromisesHandler(stream, {
        recorderType: StereoAudioRecorder,
        mimeType: 'audio/wav',
        desiredSampRate: 16000,
        audioBitsPerSecond: 256000,
        numberOfAudioChannels: 1,
      });

      setRecorder(recorderInstance);
    } catch (error) {
      console.error('Permission or initialization failed', error);
    }
  };

  // Start recording
  const startRecording = async () => {
    if (recorder) {
      await recorder.reset();
      await recorder.startRecording();
    }
  };

  // Stop recording and send audio
  const stopRecording = async () => {
    if (recorder) {
      await recorder.stopRecording();
      const audioBlob = await recorder.getBlob();
      audioChunks.current.push(audioBlob); // Storing the blob in the chunks ref
      sendAudio(audioBlob, props.conID);
    }
  };

  // Send audio file to server
  const sendAudio = async (audioBlob: Blob, conID: string) => {
    const data = new FormData();
    data.append('conID', conID);
    data.append('audio', audioBlob, 'Translation.wav');
    const config = {
      headers: {
        'content-type': 'multipart/form-data',
      },
    };

    try {
      await axios.post('/api/process-audio2', data, config)
        .then(function (response) {
          setGeminiResponse(response.data.Question); // Update the geminiResponse state

          const { Response, Question, ConfidenceScore } = response.data;

          setConversations((prev) => [
            ...prev,
            {
              aiQuestion: Question,
              userResponse: 'User response goes here', // Replace with actual response if needed
              Response,
              ConfidenceScore,
              Question,
            },
          ]);

          console.log("NEW GEMINI RESPONSE STORED");
        })
        .catch(function (error) {
          console.log(error);
        });
      console.log('Audio sent successfully');
    } catch (error) {
      console.error('Error sending audio', error);
    }
  };

  const speakPromise = new Promise((resolve) => {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(geminiResponse);
    synth.speak(utterance);

    utterance.onend = () => {
      resolve('done');
    }
  })

  // Speak the gemini response using SpeechSynthesis
  const GeminiResponse = async () => {
    speakPromise.then((message) => {
      console.log("done");
    })
  };

  // Start or stop recording based on firstRec state
  const StartStopRecord = async () => {
    await stopRecording();
    setTimeout(() => {
      startRecording();
      console.log("RECORDING STARTED");
    }, 5000);  // 5000 milliseconds = 5 seconds
  };

  // First time start
  const FirstTimeStart = async () => {
    setGeminiResponse(props.question);
    setTimeout(() => {
      startRecording();
      console.log("RECORDING STARTED");
    }, 5000);  // 5000 milliseconds = 5 seconds
    setFirstRec(false);
  };

  // useEffect hook to initialize the recorder and handle Gemini response changes
  useEffect(() => {
    getPermissionInitializeRecorder();
  }, []);

  // useEffect hook to handle Gemini response updates
  useEffect(() => {
    if (geminiResponse) {
      GeminiResponse(); // Call GeminiResponse when geminiResponse is updated
    }
  }, [geminiResponse]); // Dependency on geminiResponse


  const getScoreBackgroundColor = (score: string) => {
    const scoreValue = parseFloat(score);
    if (scoreValue >= 0.8) return 'bg-[#00C178]'; // High confidence (good)
    if (scoreValue >= 0.5) return 'bg-yellow-400'; // Medium confidence (neutral)
    return 'bg-red-400'; // Low confidence (bad)
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">

      {conversations.map((conv, index) => (
        <div key={index} className="w-full max-w-3xl mb-4">
          
          {/* AI Explanation */}
          {conv.Response && (
            <div className="p-4 bg-[#00C178] border-2 border-[#00C178] rounded-lg shadow-md mb-2 max-w-[50%]">
              <h2 className="mb-2 text-lg font-bold">AI Explanation:</h2>
              <p className="text-white">{conv.Response}</p>
            </div>
          )}

          {/* Score */}
          {conv.ConfidenceScore && (
            <div className={`p-4 border rounded-lg shadow-md mb-2 max-w-[50%] ${getScoreBackgroundColor(conv.ConfidenceScore)}`}>
              <h2 className="mb-2 text-lg font-bold">Score:</h2>
              <p className="text-white">{conv.ConfidenceScore}</p>
            </div>
          )}

          {/* AI Question */}
          <div className="ml-auto p-4 bg-[#00C178] border-2 border-[#00C178] rounded-lg shadow-md mb-2 max-w-[50%]">
            <h2 className="mb-2 text-lg font-bold">AI Question:</h2>
            <p className="text-white">{conv.aiQuestion}</p>
          </div>
        </div>
      ))}

      <div className="flex flex-col items-center px-6 py-3 bg-white border-[#25D366] rounded-lg shadow-md">
        <button className='' onClick={firstRec ? FirstTimeStart : StartStopRecord}>
          {firstRec ? "Begin" : "Stop"}
        </button>
      </div>

      <div className='bottom-0 mt-10 text-sm'>SpeakEasy can make mistakes. Information is AI-generated, not 100% accurate.</div>
    </div>
  );
};
