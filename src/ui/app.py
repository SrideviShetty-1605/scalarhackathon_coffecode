import sys, os

# Add project src folder to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json

# ----------------------------
# VOSK IMPORTS
# ----------------------------
from vosk import Model, KaldiRecognizer

# ----------------------------
# TEXT PROCESSING IMPORTS
# ----------------------------
from postprocess.filler_removal import remove_fillers
from postprocess.repetition import dedupe_repetition
from postprocess.grammar import correct_grammar
from postprocess.tone import apply_tone
from postprocess.formatting import format_text

# ----------------------------
# MODEL SETUP
# ----------------------------
MODEL_PATH = r"C:\Users\Admin\scalarhackathon_coffecode\model"
SAMPLE_RATE = 16000

print("Checking Vosk model path:", MODEL_PATH)
print("Exists:", os.path.exists(MODEL_PATH))

if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Vosk model not found at: {MODEL_PATH}")

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
recognizer.SetWords(True)

print("Vosk model loaded successfully")

# ----------------------------
# FASTAPI APP
# ----------------------------
APP = FastAPI()

APP.mount("/static", StaticFiles(directory="src/ui/static"), name="static")
templates = Jinja2Templates(directory="src/ui/templates")

# ----------------------------
# WEB UI
# ----------------------------
@APP.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ----------------------------
# WEBSOCKET ASR SERVER
# ----------------------------
@APP.websocket("/ws/asr")
async def ws_asr(ws: WebSocket):
    await ws.accept()
    print("Client connected")

    full_transcript = []  # store cleaned sentences

    await ws.send_json({"type": "ready"})

    try:
        while True:
            pcm_chunk = await ws.receive_bytes()

            # Final sentence
            if recognizer.AcceptWaveform(pcm_chunk):
                result = json.loads(recognizer.Result())
                raw_text = result.get("text", "")  # RAW with fillers

                # 1️⃣ Send RAW transcript immediately
                await ws.send_json({
                    "type": "raw",
                    "text": raw_text
                })

                # 2️⃣ Clean pipeline
                cleaned = remove_fillers(raw_text)
                cleaned = dedupe_repetition(cleaned)

                try:
                    cleaned = correct_grammar(cleaned)
                except:
                    pass

                cleaned = apply_tone(cleaned, "formal")
                cleaned = format_text(cleaned)

                # 3️⃣ Append to full clean transcript
                if cleaned.strip():
                    full_transcript.append(cleaned)

                # 4️⃣ Send cleaned + full transcript
                await ws.send_json({
                    "type": "final",
                    "text": cleaned,
                    "full_transcript": " ".join(full_transcript)
                })

            # Partial text
            else:
                partial = json.loads(recognizer.PartialResult())
                ptext = partial.get("partial", "")

                await ws.send_json({
                    "type": "partial",
                    "text": ptext
                })

    except WebSocketDisconnect:
        print("Client disconnected")
