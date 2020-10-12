import six
import socket

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s
