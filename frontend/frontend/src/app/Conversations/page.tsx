"use client"

import { useState, useEffect } from 'react';
import axios from 'axios';
import Link from 'next/link';
import Image from 'next/image';
import BackArrow from '../../public/imgs/back.svg'

type HistoryItem = {
    _id: { $oid: string };
    "question number": number;
    language: string;
    question: string;
    conId: string;
};
axios.defaults.baseURL = "http://localhost:4000";

export default function Conversations() {
    const [history, setHistory] = useState<HistoryItem[]>([]);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const response = await axios.get<HistoryItem[]>('/api/dashboard/');
                setHistory(response.data);
            } catch (error) {
                console.error('Error fetching history:', error);
            }
        };

        fetchHistory();
    }, []);

    return (
        <div className='w-[60%] mt-10 mx-auto'>
            <Link className='border-2 rounded-lg px-5 py-2 w-[20px] border-[#00C178] text-lg font-bold hover:bg-[#00C178]' href="/">Back</Link>
            <div className="m-10 bg-white mx-auto rounded-xl grid grid-cols-3 gap-4">
                {history.map((item, index) => (
                    <div key={item._id.$oid} className=" text-lg border-[#00C178] border-2 p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow">
                        <h3 className="text-lg font-bold underline-2 decoration-[#00C178] mb-2">Question {index + 1}</h3>
                        <p className="text-gray-700 mb-4">{item.question}</p>
                        <div className=' hover:decoration-black'>
                            <Link href={`/Conversations/${item.conId}`}>
                                View More
                            </Link>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
