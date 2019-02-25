import socket
import threading
import pymysql

class db(object):
	def __init__(self, db, user, password, addr):
		self.db = pymysql.connect(addr, user, password, db)
		self.cursor = self.db.cursor()
class Server(object):
	def __init__(self, addr):
		self.Socket = socket.socket()
		self.Socket.bind(addr)
		self.addr = addr
	def server_forever(self):
		self.Socket.listen(5)
		self.Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.Thread_pool = []
		while True:
			c, addr = self.Socket.accept()
			print('%s已连接' % str(addr))
			t = threading.Thread(target = self.MultiThread, args = (c,))
			t.daemon = True
			self.Thread_pool.append(t)
			t.start()
	def MultiThread(self, *args):
		c = args[0]
		while True:
			data = c.recv(1024)
			if not data:
				c.close()
				break
			#print(data.decode())
			
def main():
	addr = ('127.0.0.1',8421)
	A = Server(addr)
	DB = db('dict', 'root', '931225', addr[0])
	A.server_forever()
if __name__ == '__main__':
	main()