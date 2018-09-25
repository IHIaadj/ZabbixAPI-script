from zabbix_api import ZabbixAPI
import csv
import sys
import getpass

# Extract arguments 
frontend = sys.argv[1]

user = input('Username : ')
password = getpass.getpass('Password : ')


# Zabbix server IP address
zapi = ZabbixAPI(server=frontend)

# Zabbix Auth config for the Web frontEnd 
zapi.session.auth = (user, password)

zapi.session.verify = False

# Specify a timeout (in seconds)
zapi.timeout = 5.1

zapi.login(user, password)
print("Connected to Zabbix API Version %s" % zapi.api_version())


#Read csv file (IpAddress;visibleName)
f = csv.reader(open('hosts.csv'), delimiter=';')
for [ip,visibleName] in f:
    # Create host 
    print(ip)
    print(visibleName)
    hostcriado = zapi.host.create({
            'host' : ip,
            'name' : visibleName, 
            'status' : 0,
            # Interfaces definitions 
            'interfaces' : [{
                "type": 2,
                "main": "1",
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": 161
            }],
            'groups' : [{
                "groupid": 13
            }]    
        })
    print(hostcriado['hostids'][0])

    # Check for the interface ID 
    host_interface = zapi.hostinterface.get({'filter' : {"hostid": hostcriado['hostids'][0]}} )
    if host_interface:
        interface = host_interface[0]
        print(interface)
    else:
        print("no interface found") 

    itemtest = zapi.item.create({
        'name'  : "GigaEthernet 8-In",
        'key_' : "GigaEthernet8-In",
        'hostid' : hostcriado['hostids'][0],
        'type' :  4,
        'snmp_oid' : "1.3.6.1.2.1.2.2.1.10.1", 
        'snmp_community' : "N@ftal-RO", 
        'value_type' :  3,
        'interfaceid' :  interface['interfaceid'], 
        'delay' : "30s"
    })

    itemtest = zapi.item.create({
        'name'  : "GigaEthernet8-Out",
        'key_' : "GigaEthernet8-Out",
        'hostid' : hostcriado['hostids'][0] ,
        'type' :  4,
        'snmp_oid' : "1.3.6.1.2.1.2.2.1.16.1", 
        'snmp_community' : "N@ftal-RO", 
        'value_type' :  3,
        'interfaceid' :  interface['interfaceid'], 
        'delay' : "30s"
    })

    itemtest = zapi.item.create({
        'name'  : "GigaEthernet 9-In",
        'key_' : "GigaEthernet9-In",
        'hostid' : hostcriado['hostids'][0],
        'type' :  4,
        'snmp_oid' : "1.3.6.1.2.1.2.2.1.10.2", 
        'snmp_community' : "N@ftal-RO", 
        'value_type' : 3,
        'interfaceid' :   interface['interfaceid'], 
        'delay' : "30s"
    })

    itemtest = zapi.item.create({
        'name'  : "GigaEthernet 9-Out",
        'key_': "GigaEthernet9-Out",
        'hostid' : hostcriado['hostids'][0],
        'type' :  4,
        'snmp_oid' :  "1.3.6.1.2.1.2.2.1.16.2", 
        'snmp_community':  "N@ftal-RO", 
        'value_type' : 3,
        'interfaceid' : interface['interfaceid'], 
        'delay' : "30s"
    })

    # Get Item IDs
    host_items = zapi.item.get({'filter' : {"hostid": hostcriado['hostids'][0]}} )
    if host_items:
        items = host_items[0]
        print(items)
    else:
        print("no item found") 
    print(host_items)
    # Create Graphs 
    graph = zapi.graph.create({
        'name' : "I/O-8",
        'width' : 900, 
        'height':  200, 
        'gitems' : [{
            "itemid" : host_items[0]['itemid'], 
            "color" :"00AA00"
        },{
            "itemid" : host_items[1]['itemid'], 
            "color" :"DD0000" 
        }]
    })

    graph = zapi.graph.create({
        'name'  :  "I/O-9",
        'width' : 900, 
        'height'  : 200, 
        'gitems' : [{
            "itemid" : host_items[2]['itemid'], 
            "color" :"00AA00"
        },{
            "itemid" : host_items[3]['itemid'], 
            "color" :"DD0000" 
        }]
    })
        


    

    