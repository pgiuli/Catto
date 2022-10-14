import base64
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

def encode_message(message):
    original_message = message
    message_bytes = original_message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def decode_message(message):
    base64_message = message
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    original_message = message_bytes.decode('ascii')
    return original_message


