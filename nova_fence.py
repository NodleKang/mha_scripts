# MHA Manager 서버에서 nova_fence.py 파일을 작성한다. (경로 : power_manager_nova 와 동일 경로에 작성)
# 해당 파일은 Cloud 내 Nova 명령을 호출하여 Guest OS를 Shutdown 하므로, Cloud 관리팀과 상의 및 정상 작동여부를 위한 테스트 진행 후 적용이 필요하다.
# (즉, 해당 스크립트가 수행되면 VM은 shutoff되며 이를 재기동하기 위해서는 별도의 nova cmd 또는 Web UI 또는 API 호출을 필요로 한다.)
# nova_fence.py 및 nova_status.py는 각각 hostname을 인자로 받으며 이를 바탕으로 nova 명령을 수행한다.
# 
# 1. 즉, hostname과 openstack상의 instance name이 동일해야만 한다.
# 2. hostname과 instance name이 상이할 경우에는 MHA power_manager_nova 상에서 IP를 인자로 넘겨줄 수 있도록 변경해야 한다.
# 3. 상기 두 스크립트는 hostname 및 ip addr 두 인자에 대하여 각각 수행될 수 있도록 작성되었다.
# 4. 에러 처리는 별도 로직이 없으며 필요시 에러 handling logic 추가가 필요하다.

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
