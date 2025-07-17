import socket
import threading
from shared.config import UDP_PORT

def start_udp_chat(sock, server_ip, token, room_name, chat_username):
    def receive_messages():
        while True:
            data, _ = sock.recvfrom(4096)
            usernamelen = data[0]
            sender = data[1:1 + usernamelen].decode('utf-8')
            message = data[1 + usernamelen:].decode('utf-8')
            print(f"\n{sender}: {message}")

    threading.Thread(target=receive_messages, daemon=True).start()

    while True:
        if not token:
            print("トークンが取得されていません。先にチャットルームを作成してください。")
            break

        msg = input("> ")
        chat_username_bytes = chat_username.encode('utf-8')
        username_part = bytes([len(chat_username_bytes)]) + chat_username_bytes
        token_bytes = token.encode('utf-8')
        token_part = bytes([len(token_bytes)]) + token_bytes
        room_name_bytes = room_name.encode('utf-8')
        room_part = bytes([len(room_name_bytes)]) + room_name_bytes
        msg_bytes = msg.encode('utf-8')
        data = username_part + token_part + room_part + msg_bytes
        sock.sendto(data, (server_ip, UDP_PORT))