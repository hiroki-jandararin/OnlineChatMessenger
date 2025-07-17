def build_response(room_name, operation, state, payload_data):
    room_name_bytes = room_name.encode('utf-8')
    room_name_size = len(room_name_bytes)

    payload_bytes = payload_data.encode('utf-8')
    total_payload_bytes = room_name_bytes + payload_bytes
    payload_size = len(total_payload_bytes)

    header = bytes([room_name_size, operation, state]) + payload_size.to_bytes(29, 'big')
    return header + total_payload_bytes

def build_error_response(operation, error_message):
    payload = error_message.encode('utf-8')
    payload_size = len(payload)

    room_name_size = 0 
    state = 3

    header = (
        bytes([room_name_size, operation, state]) +
        payload_size.to_bytes(29, 'big')
    )
    return header + payload

def parse_response_header(header):
    room_name_size = header[0]
    operation = header[1]
    state = header[2]
    payload_size = int.from_bytes(header[3:32], 'big')
    return room_name_size, operation, state, payload_size