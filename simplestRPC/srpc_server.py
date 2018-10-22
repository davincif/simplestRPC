import os
import threading
from inspect import signature

import varenv
from simplestRPC.connector import Listener
from simplestRPC.auxiliar import aux


class SRPCServer:
	__con = None
	__listener = None
	__client_pool = {}
	__client_pool_lock = None
	__rpcs = {}
	__client_servers = {}
	__client_servers_lock = None
	debug = None
	__authenticator = None

	def __init__(self, debug=False, customIP=None, customPort=None, authenticator=None, encryptKey=None):
		self.debug = debug
		self.__con = Listener(
			os.getenv("SRPC_SERVER") if customIP is None else customIP,
			os.getenv("SRPC_SERVER_PORT") if customPort is None else customPort
		)

		if(self.debug):
			print('debug option is ' + str(self.debug))
			print('env var', os.getenv("SRPC_SERVER"), os.getenv("SRPC_SERVER_PORT"))
			print(self.__con)

		self.__con.listen()
		self.__client_pool_lock = threading.Lock()
		self.__client_servers_lock = threading.Lock()
		self.__listener = threading.Thread(target=self.__serve)

		# set authentication
		self.set_authentication(authenticator, encryptKey)

	def __del_(self):
		with self.__client_pool_lock:
			for client in self.__client_pool:
				self.disconnect_client(client, nolock=True)
		del self.__con
		self.__listener._stop()
		del self.__listener
		for server in self.__client_servers:
			self.__client_servers[server]._stop()
			del self.__client_servers

	def __delattr__(self, name):
		if(name == '__con'):
			self.__con.disconnect()

	def __str__(self):
		return 'client_pool: ' + str(self.__client_pool) + '\nconnection: ' + str(self.__con)

	def __serve(self):
		while True:
			if(self.debug):
				print("accpeting at ", self.__con)

			newClient = self.__con.accept()
			newClientKey = str(newClient)

			if(self.debug):
				print("new client detected at " + newClientKey)

			# authenticate client
			authenticated = True
			clientEncriptKey = None

			# warn client about server authentication status
			try:
				sent = newClient.send('>simplestRPC.auth: ' + ('yes' if self.__authenticator is not None else 'no'))
				ok = newClient.recv()

				if(self.debug):
					print('auth response: ', ok)

				if(ok[2] == 'auth'):
					if(not aux.str_to_bool(ok[3])):
						raise Exception('authentication not expected from client')
				else:
					raise Exception('authentication not expected from client')

				if(not (ok[2] == 'auth' and ok[3] == 'ok')):
					raise Exception('authentication not expected from client')
			except Exception:
				authenticated = False
			else:
				if(self.__authenticator is not None):
					# call autentication function
					(authenticated, clientEncriptKey) = self.__do_authentication(newClient)

					if(self.debug):
						print('__do_authentication')
						print('\tauthenticated: ', authenticated)
						print('\tclientEncriptKey: ', clientEncriptKey)

			# save client to pool and sync him
			if(authenticated):
				# save to pool
				with self.__client_pool_lock:
					self.__client_pool[newClientKey] = {
						'socket': newClient,
						'encriptKey': clientEncriptKey
					}

				# fetch rpc functions stats with the client
				self.update_client_rpcs(newClientKey)
				self.__serve_clients(newClientKey)
			else:
				# authorization failed or denied
				newClient.disconnect()
				del newClient

	def __client_server(self, clientKey):
		client = None

		while True:
			with self.__client_servers_lock:
				if(clientKey in self.__client_pool):
					_client = self.__client_pool[clientKey]
					client = _client['socket']
				else:
					if(self.debug):
						print('client ' + clientKey + ' was deleted. Ending thread')

					break

			try:
				msg = client.recv()[0]

				if(self.debug):
					print('from ' + str(client) + " got: ", msg)
			except Exception as err:
				self.disconnect_client(clientKey)
				break
			else:
				# separate requested function from arguments
				func, args = aux.func_args_separator(msg)

				# check argument length consistence
				if(len(args) == int(self.__rpcs[func][1])):
					try:
						response = self.__rpcs[func][0](*args)
					except Exception as err:
						response = '>simplestRPC.ERR: ' + str(err)
				else:
					response = '>simplestRPC.ERR: ' + len(args) + " given, but " + str(self.__rpcs[func][1]) + " expected"

				# sending response
				while True:
					err_counter = 0

					try:
						client.send(response)
					except Exception:
						err_counter += 1

						if(self.debug):
							print('error sending response, err_counter: ' + str(err_counter))

						# too much attempts
						if(err_counter > 2):
							self.disconnect_client(clientKey)
							break

						# try to reconect
						self.__conection_reset(self.__ip, self.__port)
					else:
						# all went fine, just quit the loop
						break

	def __serve_clients(self, clientKey):
		success = False

		if(clientKey in self.__client_pool):
			with self.__client_servers_lock:
				_client = self.__client_pool[clientKey]
				client = _client['socket']
				aux = threading.Thread(target=self.__client_server, args=[clientKey])
				aux.daemon = False
				self.__client_servers[clientKey] = aux
				self.__client_servers[clientKey].start()

			success = True

		return success

	def __do_authentication(self, newClient):
		success = True
		authKey = None

		try:
			# recive athentication argument
			clientIdent = newClient.recv()[0]
			if(clientIdent == ''):
				raise Exception('error on receive')

			if(self.debug):
				print('clientIdent:', clientIdent)

			# check if argument is empty
			(command, command_args) = aux.simplesRPC_command_finder(clientIdent)
			if(command is not None):
				if(command == 'empty'):
					clientIdent = None
				else:
					raise Exception('client args for auth not recognized: (' + str(command) + ', ' + str(command_args) + ')')
		except Exception as err:
			if(self.debug):
				print('authentication failed: ' + str(err))
			success = False
		else:
			# call authenticator
			authKey = self.__authenticator(clientIdent)

			# check its return consistency
			if(authKey is not None and type(authKey) is not str and type(authKey) is not bytes):
				raise Exception('authenticator must return None, str, bytes, empty string or False, not "' + str(type(authKey)) + '"')

			# setting authkey encoded
			if(authKey is bytes):
				authKey = authKey.decode()

			# sending authentication response
			try:
				if(authKey is None or authKey == False or authKey == ''):
					# authorization function has dineid acess for this client
					newClient.send('>simplestRPC.auth: unauthorized')
					success = False
				else:
					# successful authorization
					newClient.send(authKey)
			except Exception:
				success = False

		return (success, authKey)

	def set_authentication(self, authenticator, encryptKey=None):
		# check argument consistency
		if(not callable(authenticator) and authenticator is not None):
			raise Exception('authenticator, if not None, must be a callable object')
		else:
			self.__authenticator = authenticator

	def disconnect_client(self, ipport, nolock=False):
		if(nolock):
			if(ipport in self.__client_pool):
				self.__client_pool[ipport]['socket'].disconnect()
				del self.__client_pool[ipport]
		else:
			with self.__client_pool_lock:
				if(ipport in self.__client_pool):
					self.__client_pool[ipport]['socket'].disconnect()
					del self.__client_pool[ipport]

	def serve(self):
		self.__listener.daemon = False
		self.__listener.start()

	def add_rpc(self, func, name=None):
		if((name is None or type(name) == str) and callable(func)):
			if(name is None):
				self.__rpcs[func.__name__] = (func, len(list(signature(func).parameters)))
			else:
				self.__rpcs[name] = (func, len(list(signature(func).parameters)))

		if(self. debug):
			print('rpc added, current: ', self.__rpcs)

	def update_client_rpcs(self, clientKey):
		success = False

		if(clientKey in self.__client_pool):
			with self.__client_pool_lock:
				_client = self.__client_pool[clientKey]
				client = _client['socket']

				if(self.debug):
					print("seding these rpc's for the client: ", [(rc, self.__rpcs[rc][1]) for rc in self.__rpcs])

				sent = client.send([(rc, self.__rpcs[rc][1]) for rc in self.__rpcs])

				success = True

			if(self.debug):
				print("rpcs' sent, " + str(sent) + ' bytes')

		return success



# FOR DEV TESTING PROPOSE ONLY
if __name__ == '__main__':
	def newPrint(msg):
		print(msg)
		return msg
	# server = SRPCServer(debug=True)
	server = SRPCServer(debug=False)
	server.add_rpc(newPrint)
	server.serve()
