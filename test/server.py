from simplestRPC.srpc_server import SRPCServer

def remove_function(a, b, c):
	print(a)
	return int(b) + int(c)

server = SRPCServer()
server.add_rpc(remove_function)
server.serve()
