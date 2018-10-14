import pickle

def marshal(msg):
	return pickle.dumps(msg)

def unmarshal(obj):
	return pickle.loads(obj)

# FOR DEV TESTING PROPOSE ONLY
if __name__ == '__main__':
	a = marshal('uma mensagem qualquer')
	print(a)
	a = unmarshal(a)
	print(a)
