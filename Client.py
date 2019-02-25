import socket
import sys


class Client(object):
	def __init__(self, addr):
		self.Socket = socket.socket()
		self.addr = addr
	def start(self):
		self.Socket.connect(self.addr)
		self.Menu()
	def sign_up(self):
		pass
	def sign_in(self):
		pass
	def Menu(self):
		while True:
			print('========================欢迎使用雄牌字典========================')
			print('************************选择你需要的序号************************')
			print('************************1、注册帐号****************************')
			print('************************2、登录帐号****************************')
			print('************************3、退出词典****************************')
			how = input()
			if how == '3':
				sys.exit('客户端已退出!')
			elif how == '1':
				self.sign_up()
			elif how == '2':
				self.sign_in()
			else:
				print('您输入的命令有误，请重新输入!')
				continue
	def Sec_Menu(self):
		while True:
			print('************************您已经成功登录了************************')
			print('************************1、查询单词****************************')
			print('************************2、查询记录****************************')
			print('************************3、退出登录****************************')	
			if how == '3':
				print('登陆已注销，欢迎您继续使用!')
				break
			elif how == '1':
				self.sign_up()
			elif how == '2':
				self.sign_in()
			else:
				print('您输入的命令有误，请重新输入!')
				continue			
def main():
	addr = ('127.0.0.1',8421)
	B = Client(addr)
	B.start()
if __name__ == '__main__':
		main()	
