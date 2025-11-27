class VoskProcessor extends AudioWorkletProcessor {

    constructor() {
        super();
    }

    process(inputs, outputs, parameters) {
        const input = inputs[0];

        // No audio available
        if (!input || !input[0]) return true;

        const floatData = input[0]; // Float32Array audio

        // Convert Float32 → PCM16 buffer
        const pcm16 = new Int16Array(floatData.length);

        for (let i = 0; i < floatData.length; i++) {
            let x = Math.max(-1, Math.min(1, floatData[i]));
            pcm16[i] = x < 0 ? x * 0x8000 : x * 0x7FFF;
        }

        // Send raw bytes to script.js → WebSocket → backend
        this.port.postMessage(pcm16.buffer);

        return true; // Keep processor alive
    }
}

registerProcessor("vosk-processor", VoskProcessor);
