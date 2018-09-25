from zabbix_api import ZabbixAPI
import csv
import sys
import getpass

# Extract arguments 
frontend = sys.argv[1]

user = input('Username : ')
password = getpass.getpass('Password : ')


# Zabbix server IP address
zapi = ZabbixAPI(server= frontend)

# Zabbix Auth config for the Web frontEnd 
zapi.session.auth = (user, password)

zapi.session.verify = False

# Specify a timeout (in seconds)
zapi.timeout = 5.1

zapi.login(user, password)
print("Connected to Zabbix API Version %s" % zapi.api_version())

template = zapi.hostgroup.get({'filter' : {"name":"hostItem"}})
print(template)

