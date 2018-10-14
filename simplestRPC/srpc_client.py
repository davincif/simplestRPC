import os

import varenv
from simplestRPC.connector import Client


class SRPCClient:
	__con = None
	__rpcs = None
	__before_rpc_call = None
	__before_rpc_call_custom = None
	__after_rpc_call = None
	__after_rpc_call_custom = None
	debug = None

	def __init__(self, debug=False):
		# create and set client connection
		self.debug = debug
		self.__con = Client(os.getenv("SRPC_SERVER"), os.getenv("SRPC_SERVER_PORT"))
		self.__con.connect()

		if(self.debug):
			print('debug option is ' + str(self.debug))
			print("connected to : " + str(self.__con))
			print("waiting for rpcs")

		# rpc mechenics set
		self.__before_rpc_call = self.__standard_before_rpc_call
		self.__after_rpc_call = self.__standard_after_rpc_call

		# get rpcs from server
		self.__rpcs = self.__con.recv()[0]

		for rpc in self.__rpcs:
			def temp_name(*args):
				# return
				toRet = None

				# calling set before
				if(self.__before_rpc_call is not None):
					self.__before_rpc_call()
				if(self.__before_rpc_call_custom is not None):
					self.__before_rpc_call_custom()

				# debug
				if(self.debug):
					print('temp_name as ' + rpc[0], "args >>", args)

				# argument consistence check
				if(len(args) != int(rpc[1])):
					raise Exception(temp_name.__name__ + " receives 1 argument, but got", len(args))

				# remote call
				sent = self.__con.send(rpc[0] + str(args))

				if(self.debug):
					print('sent: ', sent)

				toRet = self.__con.recv()[0]

				# calling set after
				if(self.__after_rpc_call is not None):
					self.__after_rpc_call()
				if(self.__after_rpc_call_custom is not None):
					self.__after_rpc_call_custom()

				return toRet

			setattr(self, rpc[0], temp_name)
			temp_name.__name__ = rpc[0]

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
