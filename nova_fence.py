#!/usr/bin/env python
import sys
import socket
from os import environ as env
from novaclient.client import Client
​
def get_nova_credentials_v2():
       d = {}
       d['version'] = '2'
       d['username'] = 'openstack_dba'
       d['password'] = 'password' 
       d['auth_url'] ='https://**.**.**.**:13000/v2.0'
       d['project_id'] ='94c95a8ce5c945fg8344591a17f7f7e8'
       d['cacert'] ='/engn001/masterha/openstack_scripts/overcloud-cacert.pem'
       return d
​
credentials = get_nova_credentials_v2()
nova_client = Client(**credentials)
servers_list = nova_client.servers.list()
server_tostop = sys.argv[1]
server_exists = False
server = ""
​
try:
   socket.inet_aton(server_tostop)
   for s in servers_list:
       # use Cloud network's configuraton, private network name
       tmp = s.networks['20180415_100']
       if server_tostop == tmp[0] :
           print("This server %s exists" % server_tostop)
           server = s
           print("This server %s " % s.name)
           server_exists = True
           break
except socket.error:
   for s in servers_list:
       if s.name == server_tostop:
           print("This server %s exists" % server_tostop)
           server = s
           print("This server %s " % server.id)
           server_exists = True
           break
​
if not server_exists:
   print("server %s does not exist" % server_tostop)
else:
   print("stop server..........")
   # need to comment to test 
   nova_client.servers.stop(server)
   print("server %s stopped" % server.name)
