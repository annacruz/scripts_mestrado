#!/usr/bin/env python

from ssh_connection_util import Ssh
from bgp_table_util import Util

host = '192.169.1.101'
username = 'ubuntu'
password = 'ubuntu'
timeout = 60

command = "sudo vtysh -c 'show ip bgp'"

ssh = Ssh()
util = Util()

connection = ssh.connect(host=host, username=username, password=password, timeout=timeout)
resultSet, stderr = ssh.sudoExecute(connection, command, password)

bgpDict = util.convert_to_dict(resultSet)

print bgpDict
