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
		# create and set client connection
		self.debug = debug
		self.__con = Client(
			os.getenv("SRPC_SERVER") if customIP is None else customIP,
			os.getenv("SRPC_SERVER_PORT") if customPort is None else customPort
		)
		self.__con.connect()

		if(self.debug):
			print('debug option is ' + str(self.debug))
			print("connected to : " + str(self.__con))
			print("waiting for rpcs")

		# rpc mechenics set
		self.__before_rpc_call = self.__standard_before_rpc_call
		self.__after_rpc_call = self.__standard_after_rpc_call

		# get rpcs from server
		ret = self.__con.recv()[0]
		self.__rpcs = aux.rpcs_tuple_list_to_dict(ret)

		if(self.debug):
			print("received rpcs: ", self.__rpcs)

		for rpc in self.__rpcs:
			def temp_name(itself, youIam, *args):
				# setting up an object referece for this "method" 'cause it's actualy a function
				itself = self

				# return
				toRet = None

				# calling set before
				if(itself.__before_rpc_call is not None):
					itself.__before_rpc_call()
				if(itself.__before_rpc_call_custom is not None):
					itself.__before_rpc_call_custom()

				# debug
				if(itself.debug):
					print('temp_name as ' + rpc, "args >>", args)

				# argument consistence check
				if(len(args) != int(itself.__rpcs[youIam][0])):
					raise Exception(rpc + " receives " + str(itself.__rpcs[youIam][0]) + " argument, but got", len(args))

				# remote call request
				sent = itself.__con.send(youIam + str(args))

				if(itself.debug):
					print('sent: ', sent)

				# remote call response
				toRet = itself.__con.recv()[0]

				# calling set after
				if(itself.__after_rpc_call is not None):
					itself.__after_rpc_call()
				if(itself.__after_rpc_call_custom is not None):
					itself.__after_rpc_call_custom()

				return toRet
			self.__rpcs[rpc].append(temp_name)

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

	def call_rpc(self, funcName, *args):
		ret = None

		try:
			rpc = self.__rpcs[funcName]
		except Exception:
			raise Exception(str(funcName) + ' is not defined')
		else:
			ret = rpc[1](self, funcName, *args)

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
