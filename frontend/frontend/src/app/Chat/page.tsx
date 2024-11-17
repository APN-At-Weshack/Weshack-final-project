"use client";

import React, { useState, useEffect, useRef } from 'react';
import axios, { AxiosResponse } from "axios";
import { useRouter } from "next/navigation";
import AudioRecorder from '@/Components/AudioRecorder';

export default function Chat() {
    const [question, setQuestion] = useState<string>();
    const [currentConID, setConID] = useState<string>("");
    const router = useRouter();
    const [firstAsk, setFirstAsk] = useState<boolean>(true);

    useEffect(() => {
        if (firstAsk) {
            axios.get("api/ask-gemini")
            .then(function (response) {
                setConID(response.data.id);
                setQuestion(response.data.question);
            })
            .catch(function (error) {
                console.log(error);
            })
            setFirstAsk(false);
        }
    });

    return (
        <>
            {/* PAGE DESIGN GOES IN AudioRecorder RETURN FUNCTION */}
            {question ? <AudioRecorder conID={currentConID} question={question}/> : "Loading..."}
        </>
    );
}
