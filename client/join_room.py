import socket
import socket

from shared.config import LOCAL_HOST, TCP_PORT, UDP_PORT
from shared.protocol import build_response, parse_response_header
from client.udp_chat import start_udp_chat

def join_room(server_ip, TCP_PORT):
    login_username = input("ユーザー名を入力してください: ")
    room_name = input("ルーム名を入力してください:")
    packet = build_response(room_name,2,0,login_username)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, TCP_PORT))
    sock.sendall(packet)

    header = sock.recv(32)
    room_name_size,operation,state,payload_size= parse_response_header(header)
    body = sock.recv(room_name_size + payload_size)
    if not body:
        print("ボディが受信されませんでした。接続を閉じます。")
        sock.close()
        return
    try:
        if state == 3:  # エラー状態
            error_message = body[room_name_size:].decode('utf-8')
            print(f"サーバーエラー: {error_message}")
            sock.close()
            return None, None, None
        room_name = body[:room_name_size].decode('utf-8')
        token = body[room_name_size:].decode('utf-8')
        print(f"トークンを取得しました: {token}")
    except Exception:
        token = ""
        print("レスポンスの解析に失敗しました。")
    
    sock.close()
    return login_username, token, room_name

login_username, token, room_name = join_room(LOCAL_HOST, TCP_PORT)

server_ip = input("接続するIPアドレスを入力してください: ")
chat_username = input("チャット内のニックネームを入力してください:")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

start_udp_chat(sock, server_ip, token, room_name, chat_username)