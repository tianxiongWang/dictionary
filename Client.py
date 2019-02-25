import socket

class Client(object):
	def __init__(self, addr):
		self.Socket = socket.socket()
		self.addr = addr
	def start(self):
		self.Socket.connect(self.addr)
		self.Send()
	def Send(self):
		while True:
			data = input('input')
			self.Socket.send(data.encode())
def main():
	addr = ('127.0.0.1',8421)
	B = Client(addr)
	B.start()
if __name__ == '__main__':
		main()	
