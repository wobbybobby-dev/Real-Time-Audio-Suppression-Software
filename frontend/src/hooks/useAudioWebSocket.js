import { useState, useRef } from "react";

export const useAudioWS = (mode, strength) => {
    const [connected, setConnected] = useState(false);
    const [streaming, setStreaming] = useState(false);

    const [inputSpectrum, setInputSpectrum] = useState([]);
    const [outputSpectrum, setOutputSpectrum] = useState([]);

    const ws = useRef(null);
    const audioContextRef = useRef(null);
    const streamRef = useRef(null);
    const workletRef = useRef(null);
    const chunkBufferRef = useRef([]);

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

                if (!audioCtx || audioCtx.state === "suspended") return;

                const buffer = audioCtx.createBuffer(
                    1,
                    floatData.length,
                    audioCtx.sampleRate
                );

                buffer.getChannelData(0).set(floatData);

                const source = audioCtx.createBufferSource();
                source.buffer = buffer;
                source.connect(audioCtx.destination);

                // Real-time frame dropping logic
                const MAX_LATENCY = 0.15;
                const now = audioCtx.currentTime;

                // Hard realtime synchronization
                const targetTime = now + 0.01;

                // If queue drifts too far ahead,
                // force resync immediately
                if (
                    !audioCtx._nextTime ||
                    audioCtx._nextTime > now + MAX_LATENCY
                ) {
                    audioCtx._nextTime = targetTime;
                }
                source.start(audioCtx._nextTime);           // Schedule playback
                source.onended = () => {
                source.disconnect();
                };
                audioCtx._nextTime += buffer.duration;     // Keep next chunk tightly synced
                // Prevent long-term drift accumulation
                if (audioCtx._nextTime < now) {
                    audioCtx._nextTime = targetTime;
                }
            }
        };
    };

    const startStreaming = async () => {
        connectWS();

        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true,
        });

        streamRef.current = stream;

        // Ensure 16kHz to match backend settings
        const audioContext = new AudioContext({
            sampleRate: 16000,
        });

        audioContextRef.current = audioContext;

        const source = audioContext.createMediaStreamSource(stream);

        // Load AudioWorklet
        await audioContext.audioWorklet.addModule("/audioProcessor.js");

        // Create AudioWorkletNode
        const workletNode = new AudioWorkletNode(
            audioContext,
            "audio-capture-processor"
        );

        workletRef.current = workletNode;

        // Receive audio from worklet thread
        workletNode.port.onmessage = (event) => {
            if (ws.current?.readyState !== WebSocket.OPEN) {
                return;
            }

            // Backpressure protection
            if (ws.current.bufferedAmount > 32768) {
                return;
            }

            const chunk = event.data;

            // Append incoming samples
            const previous = chunkBufferRef.current;

            const merged = new Float32Array(
                previous.length + chunk.length
            );

            merged.set(previous, 0);
            merged.set(chunk, previous.length);

            chunkBufferRef.current = merged;

            // Send fixed 512 chunks only
            while (chunkBufferRef.current.length >= 512) {

                const sendChunk =
                    chunkBufferRef.current.slice(0, 512);

                ws.current.send(sendChunk.buffer);

                // Keep remaining samples
                chunkBufferRef.current =
                    chunkBufferRef.current.slice(512);
            }
        };

        // Prevent raw mic playback
        const dummyGain = audioContext.createGain();
        dummyGain.gain.value = 0;

        // Connect graph
        source.connect(workletNode);
        workletNode.connect(dummyGain);
        dummyGain.connect(audioContext.destination);

        setStreaming(true);
    };

    const stopStreaming = () => {
        workletRef.current?.disconnect();
        audioContextRef.current?.close();
        streamRef.current?.getTracks().forEach(track => track.stop());
        ws.current?.close();

        setStreaming(false);
        setConnected(false);

        //clearing all
        audioContextRef.current = null;
        workletRef.current = null;
        streamRef.current = null;
        chunkBufferRef.current = [];
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

    return {
        connected,
        streaming,
        startStreaming,
        stopStreaming,
        inputSpectrum,
        outputSpectrum,
        updateControl
    };
};
