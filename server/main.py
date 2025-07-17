import threading
from server.tcp_handler import start_tcp_server
from server.udp_handler import start_udp_server

if __name__ == '__main__':
    threading.Thread(target=start_tcp_server, daemon=True).start()
    start_udp_server()