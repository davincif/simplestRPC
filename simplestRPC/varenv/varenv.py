import os
import json

__CONF_FILE = os.getenv("VARENV_CONF_FILE_PATH")
if(__CONF_FILE is None):
	# __CONF_FILE = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + '/../varenv.conf.json')
	__CONF_FILE = __CONF_FILE = "./varenv.conf.json"

# load local enviroment variables
with open(__CONF_FILE, 'r') as confFile:
	conf_json = json.loads(confFile.read())
	for config in conf_json:
		if(os.getenv(config) is None):
			os.environ[config] = conf_json[config]
