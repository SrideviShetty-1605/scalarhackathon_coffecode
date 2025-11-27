// ==========================================================
// GLOBALS
// ==========================================================
let ws = null;
let audioContext = null;
let micStream = null;
let workletNode = null;
let isRunning = false;

// UI Elements
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const flushBtn = document.getElementById("flushBtn");

const rawBox = document.getElementById("rawBox");
const cleanBox = document.getElementById("cleanBox");
const fullTranscript = document.getElementById("fullTranscript");
const partialBox = document.getElementById("partialBox");
const currentSentence = document.getElementById("currentSentence");

// ==========================================================
// HELPER
// ==========================================================
function showToast(msg) {
    console.log("[INFO]", msg);
}

// ==========================================================
// START MIC (AudioWorklet)
// ==========================================================
async function startMic() {
    micStream = await navigator.mediaDevices.getUserMedia({ audio: true });

    audioContext = new AudioContext({ sampleRate: 16000 });

    await audioContext.audioWorklet.addModule("/static/worklet-processor.js");

    workletNode = new AudioWorkletNode(audioContext, "vosk-processor");

    workletNode.port.onmessage = (event) => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(event.data);
        }
    };

    const source = audioContext.createMediaStreamSource(micStream);
    source.connect(workletNode);
}

// ==========================================================
// STOP MIC
// ==========================================================
function stopMic() {
    if (micStream) micStream.getTracks().forEach(t => t.stop());
    if (audioContext) audioContext.close();
}

// ==========================================================
// OPEN WEBSOCKET
// ==========================================================
function openWS() {
    ws = new WebSocket("ws://127.0.0.1:8000/ws/asr");
    ws.binaryType = "arraybuffer";

    ws.onmessage = (event) => {
        let data = {};
        try { data = JSON.parse(event.data); } catch { return; }

        // RAW (with filler words)
        if (data.type === "raw") {
            rawBox.value = data.text;
        }

        // Partial live text
        if (data.type === "partial") {
            partialBox.value = data.text;
        }

        // Final cleaned sentence
        if (data.type === "final") {
            currentSentence.value = data.text;
            cleanBox.value = data.text;

            if (data.full_transcript)
                fullTranscript.value = data.full_transcript;
        }
    };
}

// ==========================================================
// START SESSION
// ==========================================================
async function startSession() {
    if (isRunning) return;

    openWS();
    await startMic();

    isRunning = true;
    startBtn.disabled = true;
    stopBtn.disabled = false;
}

// ==========================================================
// STOP SESSION
// ==========================================================
function stopSession() {
    isRunning = false;

    stopMic();
    if (ws) ws.close();

    startBtn.disabled = false;
    stopBtn.disabled = true;
}

// ==========================================================
// FLUSH CLEAN
// ==========================================================
function flushClean() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ cmd: "flush" }));
    }
}

// ==========================================================
// BUTTONS
// ==========================================================
startBtn.onclick = startSession;
stopBtn.onclick = stopSession;
flushBtn.onclick = flushClean;
