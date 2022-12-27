import base64


#Base64 Encoder
def encode_message(message):
    original_message = message
    message_bytes = original_message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    #print('Encoded message!')
    return base64_message
#Base64 Decoder
def decode_message(message):
    base64_message = message
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    original_message = message_bytes.decode('ascii')
    #print('Decoded message!')
    return original_message

