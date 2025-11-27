// ========== GLOBALS ==========
let ws = null;
let isRunning = false;
let audioContext = null;
let processorNode = null;
let micStream = null;

// UI elements
const btnStart = document.getElementById('btnStart');
const btnFlush = document.getElementById('btnFlush');
const btnStop = document.getElementById('btnStop');
const statusEl = document.getElementById('status');
const rawEl = document.getElementById('raw');
const transEl = document.getElementById('trans');
const chunkMsInput = document.getElementById('chunkMs');
const toastEl = document.getElementById('toast');
const shortcutsPanel = document.getElementById('shortcuts');

// ========== UI HELPERS ==========
function showToast(msg, type = 'default', ttl = 1500) {
  toastEl.className = 'toast';
  if (type === 'error') toastEl.classList.add('error');
  toastEl.textContent = msg;
  toastEl.classList.remove('hidden');
  setTimeout(() => {
    toastEl.classList.add('hidden');
  }, ttl);
}

function setStatus(text) {
  statusEl.textContent = 'status: ' + text;
}

function appendTranscript(line) {
  const timestamp = new Date().toLocaleTimeString();
  const newLine = `[${timestamp}] ${line}\n`;
  transEl.textContent = newLine + transEl.textContent;
}

// ========== MIC + AUDIO PROCESSING ==========
async function startMicStream() {
  micStream = await navigator.mediaDevices.getUserMedia({ audio: true });

  audioContext = new AudioContext({ sampleRate: 16000 });
  const source = audioContext.createMediaStreamSource(micStream);

  processorNode = audioContext.createScriptProcessor(4096, 1, 1);

  processorNode.onaudioprocess = (e) => {
    const floatData = e.inputBuffer.getChannelData(0);
    const pcm16 = floatTo16BitPCM(floatData);

    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(pcm16);
    }
  };

  source.connect(processorNode);
  processorNode.connect(audioContext.destination);
}

function floatTo16BitPCM(float32Array) {
  const pcm16 = new Int16Array(float32Array.length);
  for (let i = 0; i < float32Array.length; i++) {
    let s = Math.max(-1, Math.min(1, float32Array[i]));
    pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
  }
  return pcm16;
}

// ========== WEBSOCKET ==========
function openWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = window.location.host;
  const url = `${protocol}//${host}/ws/asr`;

  ws = new WebSocket(url);

  ws.binaryType = "arraybuffer";

  ws.onopen = () => {
    showToast("Connected");
    setStatus("connected");
  };

  ws.onmessage = (ev) => {
    let data = JSON.parse(ev.data);

    if (data.type === "ready") {
      setStatus("ready");
    }

    if (data.type === "partial") {
      rawEl.textContent = data.text;
    }

    if (data.type === "final") {
      appendTranscript(data.text);
    }
  };

  ws.onclose = () => {
    setStatus("disconnected");
    showToast("Disconnected", "error");
  };
}

// ========== START / STOP SESSION ==========
async function startSession() {
  if (isRunning) return;

  isRunning = true;

  btnStart.disabled = true;
  btnStop.disabled = false;
  btnFlush.disabled = false;

  openWebSocket();
  await startMicStream();

  setStatus("listening");
  showToast("Recording Started 🎤");
}

function stopSession() {
  isRunning = false;

  btnStart.disabled = false;
  btnStop.disabled = true;
  btnFlush.disabled = true;

  if (processorNode) processorNode.disconnect();
  if (audioContext) audioContext.close();
  if (micStream) micStream.getTracks().forEach(t => t.stop());
  if (ws) ws.close();

  processorNode = null;
  audioContext = null;
  micStream = null;

  setStatus("stopped");
  showToast("Recording Stopped");
}

// ========== FLUSH (old feature, still works) ==========
function flushChunk() {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ cmd: "demo_flush" }));
    showToast("Demo Flush sent");
  }
}

// ========== COPY / CLEAR ==========
async function copyLatest() {
  const firstLine = transEl.textContent.split('\n')[0];
  if (firstLine.trim()) {
    await navigator.clipboard.writeText(firstLine);
    showToast("Copied latest line");
  }
}

async function copyAll() {
  const txt = transEl.textContent.trim();
  if (txt) {
    await navigator.clipboard.writeText(txt);
    showToast("All text copied");
  }
}

function clearTranscripts() {
  transEl.textContent = "";
  showToast("Cleared");
}

// ========== UI EVENTS ==========
btnStart.addEventListener('click', startSession);
btnStop.addEventListener('click', stopSession);
btnFlush.addEventListener('click', flushChunk);

setStatus("idle");
shortcutsPanel.style.display = "block";
