import asyncio
import math
import fractions
import logging
from typing import List

import numpy
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer, MediaStreamTrack, RTCIceCandidate
from aiortc.contrib.media import MediaStreamTrack
from av import AudioFrame
from aiortc.mediastreams import AudioStreamTrack

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

class SineWaveTrack(AudioStreamTrack):
    def __init__(self):
        super().__init__()
        self.sample_rate = 48000
        self.samples_per_frame = 960
        self.timestamp = 0
        self.freq = 440  # Frequency of the sine wave (Hz)

    async def recv(self):
        samples = []
        for i in range(self.samples_per_frame):
            t = (self.timestamp + i) / self.sample_rate
            sample = int(32767 * math.sin(2 * math.pi * self.freq * t))
            samples.append(sample)

        frame = AudioFrame.from_ndarray(
            numpy.array(samples, dtype=numpy.int16).reshape(1, -1),
            format="s16",
            layout="mono"
        )
        frame.sample_rate = self.sample_rate
        frame.time_base = fractions.Fraction(1, self.sample_rate)
        frame.pts = self.timestamp
        
        self.timestamp += self.samples_per_frame
        return frame

@app.get("/")
async def get():
    with open("index.html", "r") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pc = RTCPeerConnection(RTCConfiguration(iceServers=[RTCIceServer(urls=["stun:stun.l.google.com:19302"])]))

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        logger.info(f"Connection state is {pc.connectionState}")
        if pc.connectionState == "failed":
            await pc.close()

    audio_track = SineWaveTrack()
    pc.addTrack(audio_track)

    try:
        while True:
            message = await websocket.receive_json()
            if message["type"] == "offer":
                logger.info("Received offer")
                offer = RTCSessionDescription(sdp=message["sdp"], type=message["type"])
                await pc.setRemoteDescription(offer)
                logger.info("Remote description set")

                answer = await pc.createAnswer()
                logger.info(f"Created answer: {answer}")

                await pc.setLocalDescription(answer)
                logger.info("Local description set")

                await websocket.send_json({
                    "type": "answer",
                    "sdp": pc.localDescription.sdp,
                })
                logger.info("Answer sent")
            elif message["type"] == "candidate":
                candidate = message["candidate"]
                logger.info(f"Received ICE candidate: {candidate}")
                if candidate is not None:
                    ice_candidate = RTCIceCandidate(
                        sdpMid=candidate.get("sdpMid"),
                        sdpMLineIndex=candidate.get("sdpMLineIndex"),
                    )
                    await pc.addIceCandidate(ice_candidate)
                    logger.info("ICE candidate added")
    except Exception as e:
        logger.exception(f"Error in WebSocket handler: {e}")
    finally:
        await pc.close()
        logger.info("Peer connection closed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")