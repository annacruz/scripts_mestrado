#!/usr/bin/env python

from ssh_connection_util import Ssh
from bgp_table_util import Util
from pymongo import MongoClient

# TODO:
#   Config file
#   Daemonize and execute from times to times

host = '192.169.1.101'
username = 'ubuntu'
password = 'ubuntu'
timeout = 60

command = "sudo vtysh -c 'show ip bgp'"

client = MongoClient('localhost', 27017)
db = client.stats
collection = db.bgp_info

ssh = Ssh()
util = Util()

connection = ssh.connect(host=host, username=username, password=password, timeout=timeout)
resultSet, stderr = ssh.sudoExecute(connection, command, password)
connection.close()
bgpDict = util.convert_to_dict(resultSet)

collection.insert(bgpDict)

print bgpDict
