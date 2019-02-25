import socket
import threading
import pymysql
import time
import hashlib


class db(object):
	def __init__(self, db, user, password, addr):
		self.database = pymysql.connect(addr, user, password, db)
		self.cursor = self.database.cursor()
class Server(object):
	def __init__(self, addr, DB):
		self.Socket = socket.socket()
		self.Socket.bind(addr)
		self.addr = addr
		self.DB = DB                     #自定义该服务器类的数据库
	def server_forever(self):
		self.Socket.listen(5)
		self.Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		while True:
			c, addr = self.Socket.accept()
			print('%s已连接' % str(addr))
			t = threading.Thread(target = self.MultiThread, args = (c,))
			t.daemon = True
			t.start()
	def MultiThread(self, *args):
		c = args[0]
		while True:
			data = c.recv(1024)
			if not data:
				print(c.getpeername(),'已退出')
				c.close()
				break
			if data == b'####':
				print(c.getpeername(),'已退出')
				break
			if data == b'!!!!':
				c.send('收到创建帐号请求!请开始你的表演!'.encode())
			else:
				msg = data.decode()
				Req = msg.split(' ')               #接受信号，并进行解析
				if Req[0] == 'CCCC':
					self.DB.cursor.execute("select count(*) from customers where name = %s",[Req[1]])
					x = self.DB.cursor.fetchone()
					if x[0] == 0:
						c.send(b'####')             #服务器的####表示没有重复用户名
						data = c.recv(1024).decode()
						s1 = hashlib.sha1()
						s1.update(data.encode('utf8'))
						password = s1.hexdigest()
						sql = "insert into customers (name, password) values (%s, %s);"
						self.DB.cursor.execute(sql, [Req[1], password])
						self.DB.database.commit()
					else:
						c.send(b'!!!!')             #服务器的！！！！表示有重复用户
				if Req[0] == 'SSSS':
					username = Req[1]
					password = Req[2]
					s1 = hashlib.sha1()
					s1.update(password.encode('utf8'))
					password = s1.hexdigest()
#					print(username,password)
					self.DB.cursor.execute("select count(*) from customers where name = %s and password = %s",[username,password])
					x = self.DB.cursor.fetchone()
					if x[0] == 1:
						c.send('OK'.encode())
					if x[0] == 0:
						c.send('No'.encode())
				if Req[0] == 'MMMM':                 #此时Req[2]是用户名,Req[1]是查询的单词
					word = Req[1]
					username = Req[2]
					sql = "select * from dictionary where word = %s"
					self.DB.cursor.execute(sql, [word])
					data = self.DB.cursor.fetchall()
					mean = ''
					for i in data:
						mean = mean + '\n' + i[1]    #获得所有的意思
					c.send(mean.encode())
					sql = "select cust_id from customers where name = %s"
					self.DB.cursor.execute(sql, [username])
					cust_id = self.DB.cursor.fetchone()[0]
					sql = "insert into log (date, cust_id, word) values (curtime(), %s, %s)"
					self.DB.cursor.execute(sql, [cust_id, word])
					self.DB.database.commit()
				if Req[0] == 'HHHH':
					sql = "select cust_id from customers where name = %s"
					self.DB.cursor.execute(sql, [username])
					cust_id = self.DB.cursor.fetchone()[0]
					sql = "select * from log where cust_id = %s"
					self.DB.cursor.execute(sql, [cust_id])
					#返回多个值为元祖的元组，每个内部元组有4个值
					history = self.DB.cursor.fetchall()
					for i in history:
						time.sleep(0.01)
						data = "date:%s,word:%s" % (i[1], i[2])	
						c.send(data.encode())
					time.sleep(0.1)
					c.send(b'######')     #自定义解码格式，表示不再发送记录
				else:
					continue


def main():
	addr = ('127.0.0.1',8888)
	DB = db('dict', 'root', '931225', addr[0])
	A = Server(addr, DB)
	A.server_forever()
if __name__ == '__main__':
	main()