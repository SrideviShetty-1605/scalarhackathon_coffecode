from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse



APP = FastAPI()

APP.mount("/static", StaticFiles(directory="src/ui/static"), name="static")
templates = Jinja2Templates(directory="src/ui/templates")

@APP.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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

