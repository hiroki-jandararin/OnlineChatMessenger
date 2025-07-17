import socket
import socket

from shared.config import LOCAL_HOST, TCP_PORT
from shared.protocol import build_response, parse_response_header
from client.udp_chat import start_udp_chat

def send_create_room_request(server_ip, TCP_PORT):
    login_username = input("ユーザー名を入力してください: ")
    print(f"DEBUG: login_username = '{login_username}'")
    room_name = input("ルーム名を入力してください:")
    print(f"[build_response] room_name='{room_name}', username='{login_username}'")
    packet = build_response(room_name, 1, 0, login_username)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, TCP_PORT))
    sock.sendall(packet)

    header = sock.recv(32)
    room_name_size,operation,state,payload_size= parse_response_header(header)
# ボディの受信
    body = sock.recv(room_name_size + payload_size)
    if not body:
        print("ボディが受信されませんでした。接続を閉じます。")
        sock.close()
        return
    try:
        room_name = body[:room_name_size].decode('utf-8')
        token = body[room_name_size:].decode('utf-8')
        print(f"トークンを取得しました: {token}")
    except Exception:
        token = ""
        print("レスポンスの解析に失敗しました。")
    
    sock.close()
    return token,room_name

token,room_name = send_create_room_request(LOCAL_HOST, TCP_PORT)

server_ip = input("接続するIPアドレスを入力してください: ")
chat_username = input("チャット内のニックネームを入力してください:")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

start_udp_chat(sock, server_ip, token, room_name, chat_username)