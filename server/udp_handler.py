# server/udp_handler.py
import socket
import time
from server.room_manager import rooms, is_valid_token
from shared.config import SERVER_ADDRESS, UDP_PORT, TIMEOUT

clients = {}

def start_udp_server():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((SERVER_ADDRESS, UDP_PORT))
    print(f"[UDP] Listening on {SERVER_ADDRESS}:{UDP_PORT}")

    while True:
        data, address = udp_sock.recvfrom(4096)
        now = time.time()
        try:
            offset = 0

            # username
            usernamelen = data[offset]
            offset += 1
            username = data[offset : offset + usernamelen].decode('utf-8')
            offset += usernamelen

            # token
            tokenlen = data[offset]
            offset += 1
            token = data[offset : offset + tokenlen].decode('utf-8')
            offset += tokenlen

            # room name
            roomlen = data[offset]
            offset += 1
            room_name = data[offset : offset + roomlen].decode('utf-8')
            offset += roomlen

            message = data[offset:].decode('utf-8')

            if not is_valid_token(room_name, token):
                print("認証に失敗しました。")
                continue

            print(f"[UDP] {username}@{room_name}: {message} from {address}")
            clients[address] = now

            # タイムアウト処理
            for addr in list(clients):
                if now - clients[addr] > TIMEOUT:
                    del clients[addr]

            for client_addr in clients:
                udp_sock.sendto(data, client_addr)

        except Exception as e:
            print("UDP デコードエラー:", e)