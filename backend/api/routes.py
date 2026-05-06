from fastapi import APIRouter, WebSocket
import numpy as np
from backend.engine.processor import MaskingEngine

router = APIRouter()
engine = MaskingEngine()

@router.websocket("/ws/audio")
async def audio_endpoint(websocket: WebSocket):
    await websocket.accept()

    mode = "focus_speech"
    strength = 0.8

    while True:
        try:
            message = await websocket.receive()

            if "bytes" in message and message["bytes"] is not None:
                audio_bytes = message["bytes"]
                audio_array = np.frombuffer(audio_bytes, dtype=np.float32)

                if audio_array.size == 0:
                    continue

                try:
                    processed_audio, mag, enhanced_mag = engine.process_chunk(
                        audio_array, mode, strength
                    )
                except Exception as e:
                    print("PROCESS ERROR:", e)
                    continue

                await websocket.send_bytes(processed_audio.tobytes())

                await websocket.send_json({
                    "input": mag.mean(axis=1).tolist(),
                    "output": enhanced_mag.mean(axis=1).tolist()
                })

            elif "text" in message and message["text"] is not None:
                import json
                payload = json.loads(message["text"])

                if payload.get("type") == "control":
                    mode = payload.get("mode", mode)
                    strength = float(payload.get("strength", strength))

        except Exception as e:
            print("[WebSocket Disconnected]", e)
            break