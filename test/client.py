from simplestRPC.srpc_client import SRPCClient

client = SRPCClient()
ret = client.remove_function('xablau!', 12, 108)
print("return: ", ret)
