#!/usr/bin/env python

## TODO:
##  1 - Connect through ssh in a server/router
##  2 - Get dict converted 'show ip bgp' from this router
##  3 - Save this in mongodb collection
##  4 - Choose an IP and search all possible networks in collection above
##  5 - Get the interface of returned ip's (through 'show ip route xxx.xxx.xxx.xxx')

from ssh_connection_util import Ssh

host = '192.169.1.101'
username = 'ubuntu'
password = 'ubuntu'
timeout = 60

command = "sudo vtysh -c 'show ip bgp'"

ssh = Ssh()
connection = ssh.connect(host=host, username=username, password=password, timeout=timeout)
resultSet, stderr = ssh.sudoExecute(connection, command, password)

print resultSet
