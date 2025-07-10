import socket
import sys
import os
import threading

server_ip = input("接続するIPアドレスを入力してください: ")
server_port = 9001
username = input("ユーザー名を入力してください: ")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def receive_messages():
    while True:
        data, _ = sock.recvfrom(4096)
        usernamelen = data[0]
        sender = data[1:1+usernamelen].decode('utf-8')
        message = data[1+usernamelen:].decode('utf-8')
        print(f"\n{sender}: {message}")
threading.Thread(target=receive_messages, daemon=True).start()

while True:
    msg = input("> ")
    username_bytes = username.encode('utf-8')
    msg_bytes = msg.encode('utf-8')
    data = bytes([len(username_bytes)]) + username_bytes + msg_bytes
    sock.sendto(data, (server_ip, server_port))