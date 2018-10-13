import re

__ip_regex = re.compile(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|)){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
__port_regex = re.compile(r"^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$")

def val_ip(ip):
	success = None
	if(type(ip) == str and re.search(__ip_regex, ip) is not None):
		success = ip
	return success

def val_port(port):
	success = None
	if(type(port) == str and re.search(__port_regex, port) is not None):
		success = int(port)
	return success
