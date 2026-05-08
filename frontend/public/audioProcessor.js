class AudioCaptureProcessor extends AudioWorkletProcessor {
    process(inputs, outputs, parameters) {
        const input = inputs[0];

        if (input.length > 0) {
            const channelData = input[0];
            // Copy buffer safely
            this.port.postMessage(new Float32Array(channelData));
        } 
        return true;
    }
}

registerProcessor("audio-capture-processor", AudioCaptureProcessor);