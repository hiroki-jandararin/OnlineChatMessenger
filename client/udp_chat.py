import threading
from client.context import ChatContext
from shared.config import UDP_PORT

def start_udp_chat(ctx: ChatContext):
    def receive_messages():
        while True:
            data, _ = ctx.sock.recvfrom(4096)
            sender ,message = parse_chat_payload(data)
            print(f"\n{sender}: {message}")

    threading.Thread(target=receive_messages, daemon=True).start()
    run_chat_loop(ctx)

def parse_chat_payload(data: bytes) -> tuple[str, str]:
    usernamelen = data[0]
    sender = data[1:1 + usernamelen].decode('utf-8')
    message = data[1 + usernamelen:].decode('utf-8')
    return sender, message
    
def run_chat_loop(ctx: ChatContext):
    try:
        while handle_chat_step(ctx):
            pass
    except KeyboardInterrupt:
        print("\nチャットを終了しました。")
        
def handle_chat_step(ctx: ChatContext,input_fn=input, print_fn=print) -> bool:
    if not ctx.token:
        print_fn("トークンが取得されていません。先にチャットルームを作成してください。")
        return False
    msg = input_fn("> ")
    payload = build_chat_payload(ctx.chat_username, ctx.token, ctx.room_name, msg)
    ctx.sock.sendto(payload, (ctx.server_ip, UDP_PORT))
    return True

def build_chat_payload(username, token, room_name, msg) -> bytes:
    username_bytes = username.encode('utf-8')
    username_part = bytes([len(username_bytes)]) + username_bytes
    token_bytes = token.encode('utf-8')
    token_part = bytes([len(token_bytes)]) + token_bytes
    room_name_bytes = room_name.encode('utf-8')
    room_part = bytes([len(room_name_bytes)]) + room_name_bytes
    msg_bytes = msg.encode('utf-8')
    payload = username_part + token_part + room_part + msg_bytes
    return payload