# simplestRPC
[![current](https://img.shields.io/badge/version-1.3.11--alpha%20-brightgreen.svg)](https://pypi.org/project/simplestRPC/) :green_heart:
[![license](https://img.shields.io/badge/license-zlib-brightgreen.svg)](https://www.zlib.net/zlib_license.html)
[![python](https://img.shields.io/badge/python-3.5+-brightgreen.svg)](https://python.org)

A simple RPC for python.

The easiest, cleanest and simplest way to creating interactions via RPC (Remove Procedure Call)

### Description

**simplestRPC** is a light Python 3 librarie, *designed* especially to *allow communications between Microservices* bypass the REST API signatures.
But it can be used in any soluction who need a simple and light weight comunication between a process and a server like: games, fancy calculators, etc...

---

### Using

##### Steps
1. Install dependencies ─ *see section bellow*
1. Create your Server
    1. Import the server class
    1. Instantiate it
    1. Add the remove calls and its names on the client
    1. Serve it
1. Create your client
    1. Import the client class
    1. Instantiate it

##### Coding

I recommend you to isolate your environment using virtualenv, but feel free to jump the 'setting' step if you what you're doing.

###### setting
```bash
> virtualenv --python=python3 virenv
> source virenv/bin/activate
> pip install simplestRPC
```

<br/>

###### server

file you_server.py
```python
from simplestRPC.srpc_server import SRPCServer


class TestClass:
	localVar = 'var in TestClass'

	def __init__(self):
		pass

	def remote_method(self, a, b, c):
		print('remote_method: ' + self.localVar + ' ' + a)
		return int(b) - int(c)


def remote_function(a, b, c):
	print("remote_function: " + a)
	return int(b) + int(c)


tclass = TestClass()

# start to listen at the port defined by the environment variable
# if you like, you would call it like this directly defining the ip/port
# server = SRPCServer(customIP='127.0.0.1', customPort=6497)
# server = SRPCServer(debug=True) #to generate debug output
server = SRPCServer()

# at the client, the funciton 'remote_function' can be called by 'remote_function'
server.add_rpc(remote_function)
# you may pass a diferent name, at the client, 'remote_method' can be called by 'customName'
server.add_rpc(tclass.remote_method, 'customName')

# start to listen on the create ip/port
server.serve()

```

output expected
```bash
remote_function: xablau!
remote_method: var in TestClass custom method
```

<br/>

###### client

file you_client.py
```python
from simplestRPC.srpc_client import SRPCClient


# conects
client = SRPCClient()

ret = client.call_rpc('remote_function', 'xablau!', 12, 108)
print("return: ", ret)

ret = client.call_rpc('customName', 'custom method', 12, 108)
print("return: ", ret)
```

output expected
```bash
return: 120
return: -96
```

<br/>

###### callbacks

file you_client.py
```python
from simplestRPC.srpc_client import SRPCClient

def do_something_before(self, a, b):
	print("I'm doing some work always before this rpc. " + str(int(a) + int(b)))

def do_something_after(self, a):
	print("Here I'm, every time after the rpc. " + str(a))

# client = SRPCClient(debug=True) #to generate debug output
# client = SRPCClient(customIP='127.0.0.1', customPort=6497)
client = SRPCClient()
client.set_before_rpc_call(do_something_before)

ret = client.call_rpc('remote_function', (10, 8), None, 'xablau!', 12, 108)
print("return: ", ret)
client.set_after_rpc_call(do_something_after)
ret = client.call_rpc('customName', (10, 8), ('!!print this!!',), 'custom method', 12, 108)
print("return: ", ret)

```

output expected
```bash
I'm doing some work always before this rpc. 18
return:  120
I'm doing some work always before this rpc. 18
Here I'm, every time after the rpc. !!print this!!
return:  -96

```

---

### Author's Note
create by me, [davincif](https://www.linkedin.com/in/davincif/), this project of first though the needs of a another professional project made by me. But it sounds so potentially useful the the community that I decided to open this package here freely distributed.

I have no intention to continue enhancing this project professionally, but would love to carry its development with the community if there's anyone interest.

So let me know if you want to help, or also if you need any formal concentiment to use this software, despite the fact that it's already free and open by terms of a very permissive license as zlib.
