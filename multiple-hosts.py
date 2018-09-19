from pyzabbix import ZabbixAPI
import csv
import sys

# Extract arguments 
frontend = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]


# Zabbix server IP address
zapi = ZabbixAPI(frontend)

# Zabbix Auth config for the Web frontEnd 
zapi.session.auth = (user, password)

zapi.session.verify = False

# Specify a timeout (in seconds)
zapi.timeout = 5.1

zapi.login(user, password)
print("Connected to Zabbix API Version %s" % zapi.api_version())


#Read csv file (hostname;IpAddress)
f = csv.reader(open('hosts.csv'), delimiter=';')
for [hostname,ip1,ip2,ip3] in f:
    # Create host 
    hostcriado = zapi.host.create(
            host= hostname,
            status= 0,
            interfaces=[{
                "type": 2,
                "main": "1",
                "useip": 1,
                "ip": ip1,
                "dns": "",
                "port": 161
            }, 
            {
                "type": 2,
                "main": "2",
                "useip": 1,
                "ip": ip2,
                "dns": "",
                "port":161
            }, 
            {
                "type": 2,
                "main": "3",
                "useip": 1,
                "ip": ip3,
                "dns": "",
                "port": 161
            }],
            groups=[{
                "groupid": 2
            }],
            templates=[{
                "templateid": 10249
            }], 
            
        )
    print(hostcriado['hostids'][0])

    # Check for the interface ID 
    host_interface = zapi.hostinterface.get(filter={"hostid": hostcriado['hostids'][0]} )
    if host_interface:
        interface = host_interface[0]
        print(interface)
    else:
        print("no interface found") 

    for i in host_interface :  
        itemtest = zapi.item.create(
            name  = "In-" + i['ip'],
            key_= "KeyIn-"+i['ip'],
            hostid = hostcriado['hostids'][0] ,
            type =  4,
            snmp_oid= "IF-MIB::ifInOctets", 
            snmp_community = "public", 
            value_type =  3,
            interfaceid =  i["interfaceid"], 
            delay = "30s"
        )

        itemtest = zapi.item.create(
            name  = "Out-"+ i['ip'],
            key_= "KeyOut-" + i['ip'],
            hostid = hostcriado['hostids'][0] ,
            type =  4,
            snmp_oid= "IF-MIB::ifOutOctets", 
            snmp_community = "public", 
            value_type =  3,
            interfaceid =  i["interfaceid"], 
            delay = "30s"
        )
        
        # Get Item IDs
        host_items = zapi.item.get(filter={"hostid": hostcriado['hostids'][0]} )
        if host_items:
            items = host_items[0]
            print(items)
        else:
            print("no item found") 

        # Create Graphs 
        graph = zapi.graph.create(
            name  = "bandwidth"+i['ip'],
            width=900, 
            height = 500, 
            gitems = [{
                "itemid" : host_items[0]['itemid'], 
                "color" :"00AA00"
            },
                "itemid" : host_items[1]['itemid'], 
                "color" :"00AA00" 
            ]
        )


    

    
