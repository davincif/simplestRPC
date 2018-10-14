import re

__ip_regex		= re.compile(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|)){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
__port_regex	= re.compile(r"^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$")
__func_regx		= re.compile(r"^(\w)+\(")
__args_regx		= re.compile(r"((\'|\")([^\t\n\r,])+(\'|\"))|((\d)+)|(\w+)")
__arg_separator	= re.compile(r"^((\s)+|(,\s))")

def val_ip(ip):
	success = None
	if(type(ip) == str and re.search(__ip_regex, ip) is not None):
		success = ip
	return success

def val_port(port):
	success = None
	if((type(port) == str and re.search(__port_regex, port) is not None) or
		(type(port) == int and port > 0 and port < 2**16 - 1)
	):
		success = int(port)
	return success

def func_args_separator(call):
	func = __func_regx.match(call).group().replace('(', '')
	args = []
	func_args = call.split("(")[1].replace(')', '')
	arg = __args_regx.match(func_args)
	while arg is not None:
		args.append(arg.group().replace("'", '').replace('"', ''))
		start = arg.end()
		func_args = func_args[start:]
		separator = __arg_separator.match(func_args)
		if(separator is not None):
			func_args = func_args[separator.end():]
		arg = __args_regx.match(func_args)



	return (func, args)

def rpcs_tuple_list_to_dict(lot):
	# lot = list of tuples
	ret = {}

	for tup in lot:
		ret[tup[0]] = [elem for elem in tup[1:]]

	return ret



if __name__ == "__main__":
	func_args_separator("__xaBlau_pavo_Ceis('vaca', 123, block)")
