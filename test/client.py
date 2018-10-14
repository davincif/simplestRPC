# for the pack developers tests
# import sys
# sys.path.append('../')

# for the user developer test
from simplestRPC.srpc_client import SRPCClient

# client = SRPCClient(debug=True)
client = SRPCClient()
ret = client.call_rpc('remote_function', 'xablau!', 12, 108)
print("return: ", ret)
ret = client.call_rpc('customName', 'custom method', 12, 108)
print("return: ", ret)
