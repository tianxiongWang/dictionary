from Class import Server

addr = ('127.0.0.1',8888)
A = Server(addr)
A.Socket.listen(5)
c,addr = A.Socket.accept()
print(addr)