from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import os
import base64
import tempfile

from services.torrent import download_torrent, save_torrent
from args import args

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        torrent_file = b""
        download_dir = os.path.abspath(f"downloaded/{args.id}")

        if not os.path.exists(download_dir):
            os.mkdir(download_dir)


        while True:
            message = await websocket.receive_text()
            print("Received message:", message)

            torrent_file = message
            torrent_file_path = save_torrent(torrent_file)

            download_torrent(torrent_file_path, download_dir)

    except WebSocketDisconnect:
        print("WebSocket connection closed")