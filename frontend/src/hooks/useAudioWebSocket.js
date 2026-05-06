import { useState, useRef } from "react";

export const useAudioWS = (mode, strength) => {
    const [connected, setConnected] = useState(false);
    const [streaming, setStreaming] = useState(false);

    const [inputSpectrum, setInputSpectrum] = useState([]);
    const [outputSpectrum, setOutputSpectrum] = useState([]);

    const ws = useRef(null);
    const audioContextRef = useRef(null);
    const processorRef = useRef(null);
    const streamRef = useRef(null);

    const connectWS = () => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) return;

        ws.current = new WebSocket("ws://localhost:8000/ws/audio");
        ws.current.binaryType = "arraybuffer";

        ws.current.onopen = () => {
            setConnected(true);
            ws.current.send(JSON.stringify({ type: "control", mode, strength }));
        };

        ws.current.onclose = () => setConnected(false);

        ws.current.onmessage = (event) => {
            // Handle Metadata (Frequency Bars)
            if (typeof event.data === "string") {
                try {
                    const data = JSON.parse(event.data);
                    
                    // The new processor prepend logic might change the 'mag' array length.
                    // We ensure we only take the most recent frames for the visualizer.
                    if (data.input && data.output) {
                        setInputSpectrum(data.input);
                        setOutputSpectrum(data.output);
                    }
                } catch (e) {
                    console.error("JSON parse error", e);
                }
            } 
            // Handle Binary Audio Data
            else {
                const audioBufferData = event.data;
                const floatData = new Float32Array(audioBufferData);
                const audioCtx = audioContextRef.current;

                if (!audioCtx || audioCtx.state === 'suspended') return;

                const buffer = audioCtx.createBuffer(1, floatData.length, audioCtx.sampleRate);
                buffer.getChannelData(0).set(floatData);

                const source = audioCtx.createBufferSource();
                source.buffer = buffer;
                source.connect(audioCtx.destination);

                const lookAheadTime = 0.1; 
                const now = audioCtx.currentTime;

                if (!audioCtx._nextTime || audioCtx._nextTime < now) {
                    audioCtx._nextTime = now + lookAheadTime;
                }

                source.start(audioCtx._nextTime);
                audioCtx._nextTime += buffer.duration;

                if (audioCtx._nextTime > now + 0.3) {
                    audioCtx._nextTime = now + lookAheadTime;
                }
            }
        };
    };

    const startStreaming = async () => {
        connectWS();

        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        streamRef.current = stream;

        // Ensure 16kHz to match backend settings
        const audioContext = new AudioContext({ sampleRate: 16000 });
        audioContextRef.current = audioContext;

        const source = audioContext.createMediaStreamSource(stream);
        
        // We use 512 to match the overlap_size in the new processor.py
        const processor = audioContext.createScriptProcessor(512, 1, 1);
        processorRef.current = processor;

        processor.onaudioprocess = (e) => {
            if (ws.current?.readyState !== WebSocket.OPEN) return;

            const inputData = e.inputBuffer.getChannelData(0);
            
            // Send raw binary data
            ws.current.send(new Float32Array(inputData).buffer);
        };

        source.connect(processor);
        processor.connect(audioContext.destination);

        setStreaming(true);
    };

    const stopStreaming = () => {
        processorRef.current?.disconnect();
        audioContextRef.current?.close();
        streamRef.current?.getTracks().forEach(track => track.stop());
        ws.current?.close();
        setStreaming(false);
        setConnected(false);
    };

    const updateControl = (newMode, newStrength) => {
        if (ws.current?.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({
                type: "control",
                mode: newMode,
                strength: newStrength
            }));
        }
    };

    return { connected, streaming, startStreaming, stopStreaming, inputSpectrum, outputSpectrum, updateControl };
};