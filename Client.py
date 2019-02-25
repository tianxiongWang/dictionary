import socket
import sys
import time


class Client(object):
	def __init__(self, addr):
		self.Socket = socket.socket()
		self.addr = addr
	def start(self):
		self.Socket.connect(self.addr)
		self.Menu()
	def sign_up(self):
		self.SendMessage('!!!!')                   #自定义解码格式，为!!!!，表示创建帐号请求
		data = self.Socket.recv(1024).decode()
		print(data)
		username = input('请输入你的用户名:')
		self.SendMessage('CCCC' + ' ' + username)  #自定义解码格式，CCCC代表发送的注册帐号
		data = self.Socket.recv(1024)
		if data == b'####':
			print('用户名不重复，输入密码:')
			password = input('请输入你的密码:')
			self.SendMessage(password)  
			print('注册完成，您现在可以登陆了!')
		if data == b'!!!!':
			print('用户名重复，已退出到主菜单!')
	def sign_in(self):
		username = input('请输入用户名:')
		password = input('请输入密码:')
		self.SendMessage('SSSS' + ' '+ username + ' ' + password)  #自定义解码格式,SSSS代表申请登陆
		data = self.Socket.recv(1024)
		if data.decode() == 'OK':
			self.Sec_Menu(username)
		else:
			print('登陆失败，用户名或密码错误!')
	def Menu(self):
		while True:
			print('========================欢迎使用雄牌字典========================')
			print('************************选择你需要的序号************************')
			print('************************1、注册帐号****************************')
			print('************************2、登录帐号****************************')
			print('************************3、退出词典****************************')
			how = input()
			if how == '3':
				self.SendMessage('####')            #自定义解码格式，为####,表示退出
				sys.exit('客户端已退出!')
			elif how == '1':
				self.sign_up()
			elif how == '2':
				self.sign_in()
			else:
				print('您输入的命令有误，请重新输入!')
				continue
	def Search(self, username):
		while True:
			word = input('请输入你要查询的单词，输入##退出，注意，您的单词会被记录，请勿输入敏感词汇哟!\n在此输入:')
			if word == '##':
				break
			self.SendMessage('MMMM' + ' ' + word + ' ' + username)                #自定义解码格式，表示查单词
			data = self.Socket.recv(1024)
			print(data.decode())
			print()
	def History(self, username):
		data = 'HHHH ' + username
		self.SendMessage(data)                   #自定义解码格式，表示查询历史记录
		while True:
			data = self.Socket.recv(1024)
			if data == b'######':
				break
			else:
				print(data.decode())
	def Sec_Menu(self, username):
		while True:
			print('************************您已经成功登录了************************')
			print('************************选择你需要的序号************************')
			print('************************1、查询单词****************************')
			print('************************2、查询记录****************************')
			print('************************3、退出登录****************************')
			how = input()				
			if how == '3':
				print('登陆已注销，欢迎您继续使用!')
				break
			elif how == '1':
				self.Search(username)
			elif how == '2':
				self.History(username)
			else:
				print('您输入的命令有误，请重新输入!')
				continue
	def SendMessage(self, string):
		time.sleep(0.1)
		self.Socket.send(string.encode())


def main():
	addr = ('127.0.0.1',8888)
	B = Client(addr)
	B.start()
if __name__ == '__main__':
		main()	