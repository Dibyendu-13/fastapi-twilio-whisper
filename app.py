import os
import json
import uuid
import aiohttp
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import websockets
import asyncio
import twilio
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 5050))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

app = FastAPI()

# WebSocket server setup
clients = []

async def process_audio(audio_payload, stream_sid, ws):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api.openai.com/v1/audio/transcriptions',
                headers={
                    'Authorization': f'Bearer {OPENAI_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={'audio': audio_payload, 'model': 'whisper-1'}
            ) as response:
                data = await response.json()
                ai_response = data['text']
                await send_to_twilio(stream_sid, ai_response, ws)
    except Exception as e:
        print(f"Error processing audio: {e}")
        await ws.send(json.dumps({'error': 'Failed to process audio'}))

async def send_to_twilio(stream_sid, response_text, ws):
    try:
        call = twilio_client.calls(stream_sid).say(response_text)
        await ws.send(json.dumps({'success': 'Response sent to Twilio'}))
    except Exception as e:
        print(f"Error sending response to Twilio: {e}")

@app.post("/twilio/events")
async def twilio_events(request: Request):
    body = await request.json()
    stream_sid = body.get('streamSid')

    # Handle incoming audio data from Twilio
    for client in clients:
        if client.open:
            await client.send(json.dumps({'audioPayload': body['audioPayload'], 'streamSid': stream_sid}))
    
    return JSONResponse(content={'status': 'success'})

async def websocket_handler(ws, path):
    clients.append(ws)
    try:
        async for message in ws:
            data = json.loads(message)
            audio_payload = data.get('audioPayload')
            stream_sid = data.get('streamSid')
            await process_audio(audio_payload, stream_sid, ws)
    except websockets.ConnectionClosed:
        pass
    finally:
        clients.remove(ws)

@app.on_event("startup")
async def startup_event():
    server = await websockets.serve(websocket_handler, "0.0.0.0", PORT)
    await server.wait_closed()

# This will start the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
