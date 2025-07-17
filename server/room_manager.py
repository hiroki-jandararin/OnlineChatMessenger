import uuid

rooms = {}
token_to_username = {}

def generate_token(room_name, username):
    return f"{room_name}_{username}_{uuid.uuid4()}"

def is_valid_token(room_name, token):
    if room_name not in rooms:
        return False
    if token == rooms[room_name].get('host_token'):
        return True
    if token in rooms[room_name].get('participants', {}):
        return True
    return False

def register_token(token, username):
    token_to_username[token] = username