from socket import socket
from typing import Optional, Callable

from utils.types import Player
from utils.player import parse_player


def send(sock: socket, msg: str) -> None:
    try:
        sock.sendall(bytes(msg, "utf-8"))
    except Exception as e:
        print(f"Exception occured while sending data: {e}")

def receive(sock: socket) -> Optional[str]:
    try:
        data = sock.recv(64)
    except Exception as e:
        print(f"Exception occured while receiving data: {e}")
        return None

    return data.decode()
