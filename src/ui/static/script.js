// Simple WebSocket + UI + Keyboard shortcuts

let ws = null;
let isRunning = false;
let lastChunkSentAt = null;

const btnStart = document.getElementById('btnStart');
const btnFlush = document.getElementById('btnFlush');
const btnStop = document.getElementById('btnStop');
const statusEl = document.getElementById('status');
const rawEl = document.getElementById('raw');
const transEl = document.getElementById('trans');
const chunkMsInput = document.getElementById('chunkMs');
const toastEl = document.getElementById('toast');
const shortcutsPanel = document.getElementById('shortcuts');

// ---------- helpers ----------

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

// ---------- websocket logic ----------

function openWebSocket() {
  if (ws && ws.readyState === WebSocket.OPEN) return;

  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = window.location.host;
  const url = `${protocol}//${host}/ws/asr`;

  ws = new WebSocket(url);
  ws.onopen = () => {
    setStatus('connected');
    showToast('Connected to server');
  };

  ws.onmessage = (ev) => {
    try {
      const data = JSON.parse(ev.data);
      if (data.type === 'ready') {
        setStatus('ready');
      } else if (data.echo !== undefined) {
        rawEl.textContent = JSON.stringify(data, null, 2);
        appendTranscript('Server: ' + JSON.stringify(data));
      } else {
        rawEl.textContent = ev.data;
      }
    } catch (e) {
      rawEl.textContent = ev.data;
    }
  };

  ws.onclose = () => {
    setStatus('disconnected');
    showToast('Disconnected', 'error');
    ws = null;
    isRunning = false;
    btnStart.disabled = false;
    btnFlush.disabled = true;
    btnStop.disabled = true;
  };

  ws.onerror = () => {
    showToast('WebSocket error', 'error', 2000);
  };
}

function closeWebSocket() {
  if (ws) {
    ws.close();
    ws = null;
  }
}

// ---------- actions ----------

function startSession() {
  if (isRunning) return;
  isRunning = true;
  btnStart.disabled = true;
  btnFlush.disabled = false;
  btnStop.disabled = false;
  openWebSocket();
  setStatus('starting');
}

function stopSession() {
  isRunning = false;
  btnStart.disabled = false;
  btnFlush.disabled = true;
  btnStop.disabled = true;
  closeWebSocket();
  setStatus('stopped');
}

function flushChunk() {
  if (!ws || ws.readyState !== WebSocket.OPEN) {
    showToast('Not connected', 'error');
    return;
  }
  const chunkMs = parseInt(chunkMsInput.value || '1000', 10);
  const payload = {
    cmd: 'demo_flush',
    sent_at: Date.now(),
    chunk_ms: chunkMs
  };
  lastChunkSentAt = payload.sent_at;
  ws.send(JSON.stringify(payload));
  showToast('Sent demo message');
}

// copy helpers
async function copyLatest() {
  const firstLine = transEl.textContent.split('\n')[0] || '';
  if (!firstLine.trim()) {
    showToast('Nothing to copy', 'error');
    return;
  }
  try {
    await navigator.clipboard.writeText(firstLine);
    showToast('Copied latest line');
  } catch (e) {
    showToast('Copy failed', 'error');
  }
}

async function copyAll() {
  const txt = transEl.textContent.trim();
  if (!txt) {
    showToast('Nothing to copy', 'error');
    return;
  }
  try {
    await navigator.clipboard.writeText(txt);
    showToast('Copied all transcripts');
  } catch (e) {
    showToast('Copy failed', 'error');
  }
}

function clearTranscripts() {
  transEl.textContent = '';
  showToast('Cleared transcripts');
}

// ---------- UI events ----------

btnStart.addEventListener('click', startSession);
btnStop.addEventListener('click', stopSession);
btnFlush.addEventListener('click', flushChunk);

// keyboard shortcuts
document.addEventListener('keydown', (ev) => {
  const meta = ev.ctrlKey || ev.metaKey;
  const key = ev.key.toLowerCase();

  const tag = document.activeElement && document.activeElement.tagName;
  const editing = (tag === 'INPUT' || tag === 'TEXTAREA' || document.activeElement.isContentEditable);

  // toggle shortcuts with ?
  if (ev.key === '?' && !editing) {
    ev.preventDefault();
    if (shortcutsPanel.style.display === 'none') {
      shortcutsPanel.style.display = 'block';
    } else {
      shortcutsPanel.style.display = 'none';
    }
    return;
  }

  if (!meta) return;

  // Ctrl/Cmd + S — start/stop
  if (key === 's') {
    ev.preventDefault();
    if (!isRunning) startSession();
    else stopSession();
    return;
  }

  // Ctrl/Cmd + F — flush
  if (key === 'f') {
    ev.preventDefault();
    flushChunk();
    return;
  }

  // Ctrl/Cmd + C — copy latest / Shift+C all
  if (key === 'c') {
    ev.preventDefault();
    if (ev.shiftKey) copyAll();
    else copyLatest();
    return;
  }

  // Ctrl/Cmd + L — clear transcripts
  if (key === 'l') {
    ev.preventDefault();
    clearTranscripts();
    return;
  }
});

// initial
shortcutsPanel.style.display = 'block';
setStatus('idle');
