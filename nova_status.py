# MHA manager 서버에서 nova_status.py 파일을 작성한다. (경로: power_manager_nova와 동일한 경로에 작성)
# Guest VM이 running일 때는 fencing status를 "on"인 것으로 SHUTOFF일 경우에는 "off"인 것으로 반환한다.
# 이는 OpenStack 환경에는 별도 fencing device를 지원하지 않으며, nova 명령을 통한 vm.stop을 진행하기 위한 상태 검사이다.

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
       d['project_id'] ='94c95a8fg5c945ea8340391f17f7f7e8'
       d['cacert'] ='/engn001/masterha/openstack_scripts/overcloud-cacert.pem'
       return d
​
credentials = get_nova_credentials_v2()
nova_client = Client(**credentials)
servers_list = nova_client.servers.list()
server_tostop = sys.argv[1]
server_exists = False
server_status = ""
​
try:
   socket.inet_aton(server_tostop)
   for s in servers_list:
      #use Cloud Network's configuration name 
       tmp = s.networks['20180415_100']
       if server_tostop == tmp[0] :
           server = s
           server_exists = True
           break
except socket.error:
   for s in servers_list:
       if s.name == server_tostop :
           server = s
           server_exists = True
           break
​
if not server_exists:
   print("server %s does not exist" % server_tostop)
   exit("unknown")
else:
   exit(server.status)
