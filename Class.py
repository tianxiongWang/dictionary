import socket
class Server(object):
	def __init__(self, addr):
		self.Socket = socket.socket()