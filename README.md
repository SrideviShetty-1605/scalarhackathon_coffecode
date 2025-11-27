# Speech Dictation Engine — Faster-Whisper WebSocket (Offline + Parallel)

Features:
- Faster-Whisper ASR
- Fully offline
- Low latency streaming
- WebSocket based (not HTTP)
- Parallel processing using multiprocessing
- Client sends stereo Int16 PCM audio
- Server transcribes chunks and returns text

## Run
uvicorn src.ui.app:APP --host 0.0.0.0 --port 8000 --reload
