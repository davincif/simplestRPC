import sys
sys.path.append('../')

# for the user developer test
from simplestRPC.srpc_client import SRPCClient

client = SRPCClient()
ret = client.call_rpc('get_user_by_email', 'davincif@davincif.com')
print(ret)
