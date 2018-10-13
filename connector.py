import socket

from auxiliar import aux

class Listener:

	__ip = None
	__port = None
	__socket = None
	__binded = False


	def __init__(self, ip, port):
		# set ip and port if given
		if(ip is not None and port is not None):
			if(not self.set_ip_port(ip, port)):
				raise Exception('ip or port is ill-formed')

		# set socket
		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def __del__(self):
		if(self.__socket is not None):
			self.disconnect()

	def __str__(self):
		return self.__ip + ':' + str(self.__port)

	def disconnect(self):
		self.__socket.close()

	def set_ip_port(self, ip, port):
		success = False

		# check if server is already in use
		if(self.is_being_used()):
			self.disconnect()
			self.__binded = False

		self.__ip = aux.val_ip(ip)
		self.__port = aux.val_port(port)

		if(self.__ip is not None and self.__port is not None):
			return True
		else:
			return False

	def listen(self, backlog):
		if(not self.__binded):
			self.__socket.bind((self.__ip, self.__port))
			self.__binded = True
		self.__socket.listen(backlog if backlog is not None else 1)

	def accept(self):
		(socket, ipport) = self.__socket.accept()
		return Conector(socket, ipport[0], ipport[1])

	def is_being_used(self):
		return self.__ip is not None and self.__port is not None and self.__binded


class Client:

	__ip = None
	__port = None
	__socket = None


	def __init__(self, ip, port):
		# set ip and port if given
		if(ip is not None and port is not None):
			if(not self.set_ip_port(ip, port)):
				raise Exception('ip or port is ill-formed')

		# set socket
		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def __del__(self):
		if(self.__socket is not None):
			self.disconnect()

	def __str__(self):
		return self.__ip + ':' + str(self.__port)

	def disconnect(self):
		self.__socket.close()

	def set_ip_port(self, ip, port):
		success = False

		if(not self.is_being_used()):
			self.__ip = aux.val_ip(ip)
			self.__port = aux.val_port(port)

			if(self.__ip is not None and self.__port is not None):
				success = True

		return success

	def connect(self):
		self.__isClient = True
		self.__socket.connect((self.__ip, self.__port))

	def send(self, msg):
		self.__socket.send(msg.encode())

	def is_being_used(self):
		return self.__ip is not None and self.__port is not None and self.__binded


class Conector:

	__ip = None
	__port = None
	__socket = None

	def __init__(self, socket, ip, port):
		self.__socket = socket
		self.__ip = ip
		self.__port = port


	def __del__(self):
		if(self.__socket is not None):
			self.disconnect()

	def __str__(self):
		return self.__ip + ':' + str(self.__port)

	def disconnect(self):
		self.__socket.close()

	def recv(self, buffsize):
		return self.__socket.recvfrom(buffsize if buffsize is not None else 1024)



# FOR DEV TESTING PROPOSE ONLY
if __name__ == '__main__':
	ip, port = "127.0.0.1", "2727"
	con = None
	if(input() == 'c'):
		# test client
		con = Client(ip, port)
		print(con)
		con.connect()
		msg = input()
		con.send(msg)
	else:
		# test server
		lis = Listener(ip, port)
		lis.listen(None)
		print(lis)
		conection = lis.accept()
		print("conection", conection)
		print(conection.recv(None))
