from flask import Flask, render_template
from deepgram import Deepgram
from dotenv import load_dotenv
import os
import asyncio
from aiohttp import web
from aiohttp_wsgi import WSGIHandler

from typing import Dict, Callable

import gptAPI




load_dotenv()

app = Flask('aioflask')


dg_client = Deepgram("9d1da47ae5d55dadfd24fbd079de517c428aac5d")



async def process_audio(fast_socket: web.WebSocketResponse):
    async def get_transcript(data: Dict) -> None:
        if 'channel' in data:
            transcript = data['channel']['alternatives'][0]['transcript']
            if "over" in transcript:
                    stopFlagFile = open("stopFlag.txt","r+")
                    stopFlagFile.truncate(0)
                    stopFlagFile.write("1")
                    stopFlagFile.close()
            with open('log.csv','a') as fd:
                fd.write(transcript)
                fd.write("\n")
        
            if transcript:
                await fast_socket.send_str(transcript)

    deepgram_socket = await connect_to_deepgram(get_transcript)

    return deepgram_socket

async def connect_to_deepgram(transcript_received_handler: Callable[[Dict], None]) -> str:
    try:
        socket = await dg_client.transcription.live({'punctuate': True, 'interim_results': False})
        socket.registerHandler(socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
        socket.registerHandler(socket.event.TRANSCRIPT_RECEIVED, transcript_received_handler)

        return socket
    except Exception as e:
        raise Exception(f'Could not open socket: {e}')

@app.route('/')
def index():
    song = os.listdir('static/music')[0]
    return render_template('index.html',song=song)

async def socket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request) 

    deepgram_socket = await process_audio(ws)



    while True:
        data = await ws.receive_bytes()
        deepgram_socket.send(data)

        stopFlagFile = open("stopFlag.txt","r+")
        stopFlag = stopFlagFile.read()


        if stopFlag == "1":
            await (gptAPI.main())
            stopFlag = "0"
        
        stopFlagFile.truncate(0)
        stopFlagFile.write(stopFlag)
        stopFlagFile.close()

  

if __name__ == "__main__":
    logFile = open("log.csv","r+")#Cleaning the file from before
    logFile.truncate(0)
    logFile.close()

    stopFlagFile = open("stopFlag.txt","r+")
    stopFlagFile.truncate(0)
    stopFlagFile.write("0")
    stopFlagFile.close()



    loop = asyncio.get_event_loop()
    aio_app = web.Application()
    wsgi = WSGIHandler(app)
    aio_app.router.add_route('*', '/{path_info: *}', wsgi.handle_request)
    aio_app.router.add_route('GET', '/listen', socket)
    web.run_app(aio_app, port=5555)