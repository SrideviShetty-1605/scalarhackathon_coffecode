# Speech Dictation Engine — Faster-Whisper WebSocket (Offline)

Features:
- Faster-Whisper ASR
- Fully offline
- Low latency streaming
- WebSocket based (not HTTP)
- Parallel processing using multiprocessing
- Client sends stereo Int16 PCM audio
- Server transcribes chunks and returns text

## Run
# 1. Clone repo
git clone https://github.com/SrideviShetty-1605/scalarhackathon_coffecode.git
cd scalarhackathon_coffecode

# 2. Create virtual environment

# Ubuntu / Mac
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
# python -m venv .venv
# .venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. (Optional) Install missing jinja2
pip install jinja2

# 5. Run the server
uvicorn src.ui.app:APP --reload

# Open in browser:
# http://127.0.0.1:8000

uvicorn src.ui.app:APP --host 0.0.0.0 --port 8000 --reload
