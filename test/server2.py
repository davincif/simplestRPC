# for the pack developers tests
import sys
sys.path.append('../')

# for the user developer test
from simplestRPC.srpc_server import SRPCServer

def authenticate(*args):
	clientIdentificator = args[0]
	if(type(clientIdentificator) is not str):
		raise Exception('authentication argument must be str not ' +str(type(clientIdentificator)))
	print(clientIdentificator)
	return "keypassword891324782377vcb"

def rpc_test(a, b):
	print('rpc_test')
	return int(a) * int(b)


# server = SRPCServer(authenticator=authenticate)
server = SRPCServer(debug=True, authenticator=authenticate)
# server.set_authentication(authenticate)

server.add_rpc(rpc_test, 'remote_procedure_in_server')

# code

server.serve()
