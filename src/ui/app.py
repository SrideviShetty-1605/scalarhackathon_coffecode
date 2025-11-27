from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import os, asyncio, json, multiprocessing
from concurrent.futures import ProcessPoolExecutor

APP = FastAPI()

APP.mount("/static", StaticFiles(directory="src/ui/static"), name="static")
APP.mount("/templates", StaticFiles(directory="src/ui/templates"), name="templates")

@APP.get("/")
async def root():
    return {"status":"running", "open":"/templates/index.html"}

@APP.websocket("/ws/asr")
async def ws_asr(ws:WebSocket):
    await ws.accept()

    try:
        await ws.send_json({"type":"ready"})
        while True:
            msg = await ws.receive_text()
            await ws.send_json({"echo":msg})

    except WebSocketDisconnect:
        print("client disconnected")

