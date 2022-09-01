
import socket

def get_free_port():
	sock = socket.socket()
	sock.bind(('', 0))
	return sock.getsockname()[1]

def build_headers(token):
	headers = {"Content-Type": "application/json"}
	headers["authorization"] = "pat " + token
	return headers






