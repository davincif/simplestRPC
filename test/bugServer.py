import sys
sys.path.append('../')

from simplestRPC.srpc_server import SRPCServer


def get_user_by_email(email):
	print('rodando -> get_user_by_email: ', email)
	return str(2)

server = SRPCServer()
server.add_rpc(get_user_by_email)
server.serve()
