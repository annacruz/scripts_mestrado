#!/usr/bin/env python

from ssh_connection_util import Ssh
from bgp_table_util import Util
from pymongo import MongoClient
import json

# TODO:
#   Config file
#   Daemonize and execute from times to times


config = json.load(open("config/config.cfg"))

hosts     = config['host']
username  = config['username']
password  = config['password']
timeout   = config['timeout']
command   = "sudo vtysh -c 'show ip bgp'"

client     = MongoClient('localhost', 27017)
db         = client.stats
collection = db.bgp_info

ssh  = Ssh()
util = Util()

for host in hosts:
  connection = ssh.connect(host=host, username=username, password=password, timeout=timeout)
  resultSet, stderr = ssh.sudoExecute(connection, command, password)
  connection.close()
  bgpDict = util.convert_to_dict(resultSet, host)

  collection.insert(bgpDict)
