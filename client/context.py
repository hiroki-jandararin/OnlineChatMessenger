from dataclasses import dataclass

@dataclass
class ChatContext:
    sock: any
    server_ip: str
    token: str
    room_name: str
    chat_username: str