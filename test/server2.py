# for the pack developers tests
import sys
sys.path.append('../')

# for the user developer test
from simplestRPC.srpc_server import SRPCServer


server = SRPCServer()

# code

server.serve()
