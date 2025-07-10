import socket
import os
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001

print('Starting up on {} port {}'.format(server_address, server_port))
sock.bind((server_address, server_port))

print("UDP server is running and waiting for messages...")
clients = {}
timeout = 60

while True:
    data, address = sock.recvfrom(4096)
    print(f"受信したデータ: {data.decode()} from {address}")

    clients[address] = time.time()
    now = time.time()
    for addr in list(clients):
        if now - clients[addr] > timeout:
            del clients[addr]

    if data:
        usernamelen = data[0]
        username = data[1:1+usernamelen].decode('utf-8')
        message = data[1+usernamelen:].decode('utf-8')
        for client_addr in clients:
            if client_addr != address:
                sock.sendto(data, client_addr)
                print(f"Sending message to {client_addr}: {username}: {message}")
        sock.sendto(data, address)  # クライアントに返信  
        # print(f"返信データ: {data.decode()} sent back to {address}")