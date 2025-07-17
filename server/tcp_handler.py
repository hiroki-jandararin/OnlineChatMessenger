# server/tcp_handler.py
import socket
import threading
from shared.config import SERVER_ADDRESS, TCP_PORT
from shared.protocol import build_response, parse_response_header, build_error_response
from server.room_manager import register_token, rooms, token_to_username, generate_token

def handle_tcp_connection(connection, client_address):
    try:
        header = connection.recv(32)
        if not header or len(header) < 32:
            print("不完全なヘッダー。接続を閉じます。")
            return
        room_name_size, operation, state, payload_size = parse_response_header(header)
        print(f"[DEBUG] Parsed header - room_name_size: {room_name_size}, op: {operation}, state: {state}, payload_size: {payload_size}")
        body = connection.recv(payload_size)
        if not body:
            print("ボディが受信されませんでした。")
            return
        print(f"[DEBUG] Raw body bytes: {body}")
        room_name = body[:room_name_size].decode('utf-8')
        username = body[room_name_size:].decode('utf-8')
        print(f"TCP処理: room={room_name}, op={operation}, state={state}, user={username}")

        if operation == 1:  # ルーム作成
            handle_room_creation(connection, room_name, username, state)
        elif operation == 2:  # ルーム参加
            handle_room_join(connection, room_name, username, state, client_address)
        else:
            error = build_error_response(operation, "不明なオペレーションです。")
            connection.sendall(error)
    finally:
        connection.close()

def handle_room_creation(conn, room_name, username, state):
    if state == 0:
        if room_name in rooms:
            error = build_error_response(1, f"ルーム '{room_name}' はすでに存在します。")
            conn.sendall(error)
            return
        token = generate_token(room_name, username)
        register_token(token, username)
        rooms[room_name] = {
            'host_token': token,
            'participants': {},
            'users': [username]
        }
        conn.sendall(build_response(room_name, 1, 2, token))
    elif state == 1:
        conn.sendall(build_response(room_name, 1, 1, "OK"))
    else:
        conn.sendall(build_error_response(1, "不明なステータスです。"))

def handle_room_join(conn, room_name, username, state, client_address):
    if room_name not in rooms:
        conn.sendall(build_error_response(2, "ルームが存在しません。"))
        return

    if state == 0:
        for existing_token, info in rooms[room_name]['participants'].items():
            if info['username'] == username:
                if info['address'][0] == client_address[0]:
                    conn.sendall(build_response(room_name, 2, 2, existing_token))
                    return
                else:
                    conn.sendall(build_error_response(2, "このユーザー名は既に参加しています。"))
                    return
        token = generate_token(room_name, username)
        register_token(token, username)
        rooms[room_name]['participants'][token] = {'username': username, 'address': client_address}
        conn.sendall(build_response(room_name, 2, 2, token))
    else:
        conn.sendall(build_error_response(2, "無効なステータスです。"))

def start_tcp_server():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind((SERVER_ADDRESS, TCP_PORT))
    tcp_sock.listen()
    print(f"[TCP] Listening on {SERVER_ADDRESS}:{TCP_PORT}")

    while True:
        conn, addr = tcp_sock.accept()
        print(f"[TCP] 接続 from {addr}")
        threading.Thread(target=handle_tcp_connection, args=(conn, addr), daemon=True).start()