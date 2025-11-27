from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json


from vosk import Model, KaldiRecognizer
import os

# --- HARD-CODED ABSOLUTE PATH FIX ---
MODEL_PATH = r"C:\Users\Admin\scalarhackathon_coffecode\model"
SAMPLE_RATE = 16000

print("🔍 Checking:", MODEL_PATH)
print("Exists?", os.path.exists(MODEL_PATH))
print("Files inside model:", os.listdir(MODEL_PATH))

if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"❌ Vosk model not found at: {MODEL_PATH}")

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
recognizer.SetWords(True)

print("🎉 Vosk model loaded successfully!")


# ----------------------------
# FASTAPI APP
# ----------------------------
APP = FastAPI()

APP.mount("/static", StaticFiles(directory="src/ui/static"), name="static")
templates = Jinja2Templates(directory="src/ui/templates")


# ----------------------------
# INDEX ROUTE
# ----------------------------
@APP.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ----------------------------
# WEBSOCKET ROUTE FOR LIVE ASR
# ----------------------------
@APP.websocket("/ws/asr")
async def ws_asr(ws: WebSocket):
    await ws.accept()
    print("🔗 Client connected")

    # Notify frontend that ASR is ready
    await ws.send_json({"type": "ready"})

    try:
        while True:
            # Receive PCM audio chunk from frontend
            pcm_chunk = await ws.receive_bytes()

            # Feed to recognizer
            if recognizer.AcceptWaveform(pcm_chunk):
                # Final text after pause
                result_json = json.loads(recognizer.Result())
                text = result_json.get("text", "")
                await ws.send_json({
                    "type": "final",
                    "text": text
                })
            else:
                # Partial live text
                partial_json = json.loads(recognizer.PartialResult())
                partial_text = partial_json.get("partial", "")
                await ws.send_json({
                    "type": "partial",
                    "text": partial_text
                })

    except WebSocketDisconnect:
        print("❌ Client disconnected")

