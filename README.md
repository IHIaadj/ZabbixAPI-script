# ZabbixAPI-script
This script was creating as part of an internship in NAFTAL-SPA. The script uses ZabbixAPI to create multiple hosts with their associated items. 

## Zabbix 
Zabbix is an enterprise-class open source distributed monitoring solution.

Zabbix is software that monitors numerous parameters of a network and the health and integrity of servers. Zabbix uses a flexible notification mechanism that allows users to configure e-mail based alerts for virtually any event. This allows a fast reaction to server problems. Zabbix offers excellent reporting and data visualisation features based on the stored data. This makes Zabbix ideal for capacity planning.

## Requirements 
  - Python 3.6 
  - unicodecsv==0.14.1
  - zabbix-api  
  - CSV file format should be : (IPAddress;VisibleHostName)
  
## Example 
  1. Fill the CSV File with some hosts 
  2. Install the dependencies : 
    * `pip install unicodecsv`
    * `pip install zabbix-api`
  3. Run the script and enter the frontend server address in the arguments :
    `python multiple-hosts.py http://server-ip-address/zabbix `
  4. Enter the frontend server credentials as required. 
  5. Enter the group name of the hosts, for example : "Linux servers"
  6. The script automatically creates all hosts in the list with the In/Out items and graphs. 
  
## Note 
 You can customize the items and graphs by modifying directly the script.
