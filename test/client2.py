# for the pack developers tests
import sys
sys.path.append('../')

# for the user developer test
from simplestRPC.srpc_client import SRPCClient

# client = SRPCClient(debug=True, authArgs='keypassword891324782377vcb')
client = SRPCClient(authArgs='keypassword891324782377vcb')

ret = client.call_rpc('remote_procedure_in_server', 70, 7)
print(ret)
