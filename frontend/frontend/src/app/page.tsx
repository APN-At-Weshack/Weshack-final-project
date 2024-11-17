"use client";

import Logo from '../public/imgs/SpeakEasy 2.svg'

// Dynamically import the AudioRecorder component with SSR disabled

import Link from "next/link";
import axios from "axios";
import Image from 'next/image'
axios.defaults.baseURL = "http://localhost:4000";

export default function Home() {
  return (
    <>
      <div className="min-h-screen flex flex-col h-screen justify-between">
        <div className="container mx-auto">
          <div className=" font-bold text-3xl items-center mx-auto mt-10"><Image className='mx-auto' src={Logo} alt='logo' width={300} height={500} /></div>
          <div className="w-[50%] flex flex-col space-y-8 text-center mt-20 mx-auto">
            <div className='border-[2px] font-semibold text-xl px-8 py-6 rounded-lg border-[#00C178]'>
              Learn languages via conversations. Choose your language and start improving with interactive exercises and real-life scenarios.
            </div>
            <div>
              <div className="underline text-lg decoration-[#00C178]">
                Select Language: <span className="font-bold">English</span></div>
            </div>
            <div className='flex flex-col space-y-2'>
              <Link className="w-[20%] mx-auto bg-[#00C178] hover:bg-black font-bold text-white px-8 py-3 rounded-lg text-2xl border-black" href="/Chat" >Start</Link>
              <Link className="w-[30%] mx-auto underline font-bold decoration-[#00C178] decoration-2 hover:decoration-black text-lg" href="/Conversations">Past Conversations</Link>
            </div>

          </div>
        </div>
        {/* Footer */}
        <footer className="border-t-2 border-[#00C178] text-black p-4 align-bottom text-center">
          &copy; 2024 APN - WesHack2024. All rights reserved.
        </footer>
      </div>
    </>
  );
}
