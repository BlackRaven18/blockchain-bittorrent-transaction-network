from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import json
from typing import List

from schemas.client import Client
from schemas.transaction import Transaction
from schemas.block import Block

from repositories.client import add_client, get_client

from services.cryptography import verify_transaction
from services.blockchain import conduct_vote, save_transaction, save_block, check_if_should_mine_block, mine_block, cancel_mine_block, verify_block
from services.network import broadcast_action, send_file_to_client
from services.torrent import create_torrent

from clients.logger import log, MessageType
from clients.torrent import TorrentClient

from error_flags import ErrorFlags

from utils.file import decode_and_save_file

router = APIRouter()
torrent_client = TorrentClient()


active_connections: List[WebSocket] = []
log_queue = []

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
        
    try:
        while True:
            message = await websocket.receive_text()
            
            if ErrorFlags().node_damage_error:
                await websocket.send_text("Node damage error")
                continue

            response = await handle_message(message)

            if response is not None:
                await websocket.send_text(response)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def handle_message(message: str):
    """Handle incoming WebSocket messages."""
    try:
        data = json.loads(message)
        action = data.get("type")
        payload = data.get("data")

        """ 
        response is a message that will be send to the client via websocket, 
        so if user don't read it, it will remain in websocket queue.
        response should be created only if user will read it!
        """

        response = None
        #-------------------------------------------------------------------------------
        # External actions (from clients)
        #-------------------------------------------------------------------------------
        if action == "new-transaction-proposal":

            transaction = Transaction(**json.loads(payload))

            await log(MessageType.CONDUCTING_VOTE)
            result = await conduct_vote(transaction)

            if result == "Transaction accepted":
                recipient = get_client(transaction.recipient)

                full_file_name = decode_and_save_file(transaction.data, transaction.sender, transaction.recipient)
                # create torrent
                torrent_file_path, torrent_file_content, torrent_name = torrent_client.create_torrent(full_file_name)

                await broadcast_action(
                    "create-torrent", 
                    {
                        "file": transaction.data,
                        "sender": transaction.sender,
                        "recipient": transaction.recipient
                    }, 
                    False
                )
                full_file_name = decode_and_save_file(transaction.data, transaction.sender, transaction.recipient)

                torrent_file_path = torrent_client.create_torrent(full_file_name)

                await broadcast_action("seed-torrent", {"torrent_file_name": torrent_name}, False)
                await send_file_to_client(recipient.host, recipient.port, torrent_file_content)

            await log(MessageType.IDLE)

            response = result

            await check_if_should_mine_block()

        elif action == "register-client":

            print("Adding public key...")
            print(payload)
            response = await broadcast_action("accept-client", payload)
            response = response[0]
            
        #-------------------------------------------------------------------------------
        # Internal actions (from other nodes)
        #-------------------------------------------------------------------------------
        elif action == "vote":
            await log(MessageType.VOTING)
            transaction = Transaction(**json.loads(payload))

            if ErrorFlags().transaction_vote_error:
                await log(MessageType.IDLE)
                return "invalid"
            
            result = verify_transaction(transaction)
            response = result

            await log(MessageType.IDLE)

        elif action == "accept-transaction":
            await log(MessageType.SAVING_TRANSACTION)
            transaction = Transaction(**json.loads(payload))
            response = save_transaction(transaction)

            await log(MessageType.IDLE)

        elif action == "accept-client":
            await log(MessageType.ADDING_CLIENT
                      )
            client = Client(**json.loads(payload))
            response = add_client(client)

            await log(MessageType.IDLE)
            
        elif action == "mine-block":

            if ErrorFlags().block_mining_error:
                await log(MessageType.IDLE)
                return response
            
            await log(MessageType.MINING)
            
            mine_block()

        elif action == "cancel-and-verify-block":
            await log(MessageType.VERIFING_BLOCK)
            cancel_mine_block()
            response = verify_block(Block(**json.loads(payload)))

            await log(MessageType.IDLE)

        elif action == "accept-block":
            await log(MessageType.SAVING_BLOCK)

            save_block(Block(**json.loads(payload)))
            print("Block added to the blockchain")

            await log(MessageType.IDLE)

        elif action == "create-torrent":
            print("Creating torrent...")

            # save file
            full_file_name = decode_and_save_file(payload["file"], payload["sender"], payload["recipient"])
            # create torrent
            _, _, _ = torrent_client.create_torrent(full_file_name)

        elif action == "seed-torrent":
            print("Seeding torrent...")
            torrent_file_name = payload["torrent_file_name"]
            torrent_client.seed_torrent(torrent_file_name)

        else:
            print(f"Unknown action: {action}")

        print("Response: " + str(response))
        return response
    except json.JSONDecodeError:
        print("Invalid message format received.")