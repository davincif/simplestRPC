import socket

from simplestRPC.auxiliar import aux
from simplestRPC import marshaller

class Listener:

	__ip = None
	__port = None
	__socket = None
	__binded = False

	def __init__(self, ip=None, port=None):
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

		if(ip is not None):
			self.__ip = aux.val_ip(ip)
		if(port is not None):
			self.__port = aux.val_port(port)

		if(self.__ip is not None and self.__port is not None):
			return True
		else:
			return False

	def listen(self, backlog=None):
		if(not self.__binded):
			self.__socket.bind((self.__ip, self.__port))
			self.__binded = True
		self.__socket.listen(backlog if backlog is not None else 1)

	def accept(self):
		(socket, ipport) = self.__socket.accept()
		return Client(ipport[0], ipport[1], socket)

	def is_being_used(self):
		return self.__ip is not None and self.__port is not None and self.__binded


class Client:

	__ip = None
	__port = None
	__socket = None
	__befora_rpc = None

	def __init__(self, ip=None, port=None, builtSocket=None):
		# set ip and port if given
		if(ip is not None and port is not None):
			if(not self.set_ip_port(ip, port)):
				raise Exception('ip or port is ill-formed')

		# set socket
		if(builtSocket is None):
			self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.__socket = builtSocket

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
			if(ip is not None):
				self.__ip = aux.val_ip(ip)
			if(port is not None):
				self.__port = aux.val_port(port)

			if(self.__ip is not None and self.__port is not None):
				success = True

		return success

	def connect(self):
		self.__isClient = True
		self.__socket.connect((self.__ip, self.__port))

	def send(self, msg):
		sent = None

		try:
			sent = self.__socket.sendall(marshaller.marshal(msg))
		except Exception as err:
			raise err

		return sent

	def recv(self, buffsize=None):
		msg = ''
		count = 0

		while msg == '' or msg is None:
			if(count == 2):
				raise Exception("coneciton closed")

			ret = self.__socket.recvfrom(buffsize if buffsize is not None else 1024)

			try:
				msg = ret[0].decode()
			except Exception:
				msg = marshaller.unmarshal(ret[0])
			else:
				if(msg != ''):
					msg = marshaller.unmarshal(ret[0])
			count += 1

		return (msg, ret[1])

	def is_being_used(self):
		return self.__ip is not None and self.__port is not None and self.__binded

	def get_ip(self):
		return self.__ip

	def get_port(self):
		return self.__port



# FOR DEV TESTING PROPOSE ONLY
if __name__ == '__main__':
	def test_func():
		print('FUNFOOOU')

	ip, port = "127.0.0.1", "2728"
	if(input() == 'c'):
		# test client
		con = Client(ip, port)
		print(con)
		con.connect()
		# msg = input()
		con.send(test_func)
		con.disconnect()
	else:
		# test server
		lis = Listener(ip, port)
		lis.listen()
		print(lis)
		conection = lis.accept()
		print("conection", conection)
		# print(conection.recv(None))
		print(conection.recv(None)[0]())
		lis.disconnect()
		conection.disconnect()
