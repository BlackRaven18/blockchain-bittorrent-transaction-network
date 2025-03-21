from network.WebSocketClient import WebSocketClient
from typing import List

class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ConnectionsManager(metaclass=SingletonMeta):
    def __init__(self):
        self.web_socket_clients: List[WebSocketClient] = []

    def add_connection(self, web_socket_client: WebSocketClient):
        print("Adding connection...")
        self.web_socket_clients.append(web_socket_client)

    def remove_connection(self, web_socket_client: WebSocketClient):
        print("Removing connection...")
        self.web_socket_clients.remove(web_socket_client)

    async def send_and_receive_from_all(self, message: str):
        responses = []
        for web_socket_client in self.web_socket_clients:
            response = await web_socket_client.send_and_receive(message)
            responses.append(response)
        return responses
    
    async def send_to_all(self, message: str):
        for web_socket_client in self.web_socket_clients:
            await web_socket_client.send(message)
