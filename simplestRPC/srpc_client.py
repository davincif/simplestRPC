import os

import varenv
from simplestRPC.connector import Client
from simplestRPC.auxiliar import aux

class SRPCClient:
	__con = None
	__rpcs = None
	__before_rpc_call = None
	__before_rpc_call_custom = None
	__after_rpc_call = None
	__after_rpc_call_custom = None
	debug = None


	def __init__(self, debug=False, customIP=None, customPort=None):
		self.debug = debug

		# rpc mechenics set
		self.__before_rpc_call = self.__standard_before_rpc_call
		self.__after_rpc_call = self.__standard_after_rpc_call

		# create and set client connection
		self.__conection_reset(customIP, customPort)

	def __conection_reset(self, customIP=None, customPort=None):
		# check if socker is already up
		if(self.__con is not None):
			self.__con.disconnect()

		self.__con = Client(
			os.getenv("SRPC_SERVER") if customIP is None else customIP,
			os.getenv("SRPC_SERVER_PORT") if customPort is None else customPort
		)
		self.__con.connect()

		if(self.debug):
			print('debug option is ' + str(self.debug))
			print("connected to : " + str(self.__con))
			print("waiting for rpcs")

		# get rpcs from server
		ret = self.__con.recv()[0]
		self.__rpcs = aux.rpcs_tuple_list_to_dict(ret)

		if(self.debug):
			print("received rpcs: ", self.__rpcs)

		# for rpc in self.__rpcs:
		# 	self.__rpcs[rpc].append(self.generic_funciton)

		if(self.debug):
			print("done!")
			print("rpcs ->", self.__rpcs)

	def __delattr__(self, name):
		if(name == '__con'):
			self.__con.disconnect()

	def __str__(self):
		return 'connected with: ' + str(self.__con)

	def __standard_before_rpc_call(self):
		pass

	def __standard_after_rpc_call(self):
		pass

	def __generic_funciton(self, youIam, before_call_args, after_call_args, *args):
		# return
		toRet = None

		# check arguments consistency
		# if(before_call_args is not None and type(before_call_args) != tuple):
		# 	raise AttributeError("before_call_args mus be a tuple. Try put all arguments your function need in a tuple, don't worry, you'll not receive a tuple in your function")
		# if(after_call_args is not None and type(after_call_args) != tuple):
		# 	raise AttributeError("after_call_args mus be a tuple. Try put all arguments your function need in a tuple, don't worry, you'll not receive a tuple in your function")

		# calling set before
		if(self.__before_rpc_call is not None):
			self.__before_rpc_call()
		if(self.__before_rpc_call_custom is not None):
			self.__before_rpc_call_custom(*before_call_args)

		# debug
		if(self.debug):
			print('__generic_funciton named as ' + rpc, "with args >>", args)

		# argument consistence check
		if(len(args) != int(self.__rpcs[youIam][0])):
			raise Exception(rpc + " receives " + str(self.__rpcs[youIam][0]) + " argument, but got", len(args))

		# remote call request
		while True:
			err_counter = 0

			# seding call
			try:
				sent = self.__con.send(youIam + str(args))
			except Exception:
				err_counter += 1

				if(self.debug):
					print('error requesting rpc, err_counter: ' + str(err_counter))

				# too much attempts
				if(err_counter > 2):
					raise Exception('Connection lost with the server and unable to reconnect')

				# try to reconect
				self.__conection_reset(self.__ip, self.__port)
			else:
				# all went fine, just quit the loop
				break

		if(self.debug):
			print('sent: ', sent)

		# remote call response
		try:
			toRet = self.__con.recv()[0]
		except Exception as err:
			self.disconnect()
			raise Exception('Connection lost with the server and unable to reconnect')

		# check for erros at the server
		if(type(toRet) is str and ">simplestRPC.ERR:" in toRet):
			raise Exception(toRet)

		# calling set after
		if(self.__after_rpc_call is not None):
			self.__after_rpc_call()
		if(self.__after_rpc_call_custom is not None):
			self.__after_rpc_call_custom(*after_call_args)

		return toRet

	def call_rpc(self, funcName, *args):
		ret = None

		# treating potential argumetns for callback functions
		after_call_args = None
		before_call_args = args[:1][0]
		if(before_call_args is not None and type(before_call_args) == tuple):
			after_call_args = args[1:2][0]
			if(after_call_args is not None and type(after_call_args) == tuple):
				args = args[2:]
			else:
				args = args[1:]
				after_call_args = None
		else:
			before_call_args = None

		try:
			rpc = self.__rpcs[funcName]
		except Exception:
			raise Exception(str(funcName) + ' is not defined')
		else:
			ret = self.__generic_funciton(funcName, before_call_args, after_call_args, *args)

		return ret


	def set_before_rpc_call(self, func, isStandard=False):
		if(callable(func)):
			if(isStandard):
				self.__before_rpc_call = None
			self.__before_rpc_call_custom = func
		else:
			raise Exception('argument func must be callable')

	def set_after_rpc_call(self, func, isStandard=False):
		if(callable(func)):
			if(isStandard):
				self.__after_rpc_call = None
			self.__after_rpc_call_custom = func
		else:
			raise Exception('argument func must be callable')



# FOR DEV TESTING PROPOSE ONLY
if __name__ == '__main__':
	# client = SRPCClient(debug=True)
	client = SRPCClient()
	ret = client.newPrint('xablau!')
	print("return: ", ret)
