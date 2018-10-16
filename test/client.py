# for the pack developers tests
import sys
sys.path.append('../')

# for the user developer test
from simplestRPC.srpc_client import SRPCClient

def do_something_before(self, a, b):
	print("I'm doing some work always before this rpc. " + str(int(a) + int(b)))

def do_something_after(self, a):
	print("Here I'm, every time after the rpc. " + str(a))

# client = SRPCClient(debug=True)
# client = SRPCClient(customIP='127.0.0.1', customPort=6497)
client = SRPCClient()
client.set_before_rpc_call(do_something_before)

ret = client.call_rpc('remote_function', (10, 8), None, 'xablau!', 12, 108)
print("return: ", ret)
client.set_after_rpc_call(do_something_after)
ret = client.call_rpc('customName', (10, 8), ('!!print this!!',), 'custom method', 12, 108)
print("return: ", ret)
