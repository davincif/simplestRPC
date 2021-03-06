# for the pack developers tests
import sys
sys.path.append('../')

# for the user developer test
from simplestRPC.srpc_server import SRPCServer

class TestClass:
	bla = 'bla in TestClass'

	def __init__(self):
		pass

	def remote_method(self, a, b, c):
		print('remote_method: ' + self.bla + ' ' + a)
		return int(b) - int(c)


def remote_function(a, b, c):
	print("remote_function: " + a)
	return int(b) + int(c)

# server = SRPCServer(debug=True)
# server = SRPCServer(customIP='127.0.0.1', customPort=6497)
# server = SRPCServer()
server = SRPCServer(customIP="localhost")
tclass =  TestClass()
server.add_rpc(remote_function)
server.add_rpc(tclass.remote_method, 'customName')
server.serve()
