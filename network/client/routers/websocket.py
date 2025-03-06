from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import base64
import os

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        file_content = b""

        while True:
            message = await websocket.receive_text()
            print("Received message:", message)

            file_content += base64.b64decode(message)

            # if message == "EOF":
            #     print("Received EOF, saving file...")
            with open("received_file.txt", "wb") as f:
                f.write(file_content)

    except WebSocketDisconnect:
        print("WebSocket connection closed")