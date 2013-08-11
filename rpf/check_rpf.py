#! /usr/bin/env python

from ssh_connection_util import Ssh
from bgp_table_util import Util

from pymongo import MongoClient
import re
import sys
import ipaddress
import json

global config
config = json.load(open("config/config.cfg"))

def execute(entrance):
  """ Connects to the mongodb database and checks if the entrance ip has the first digits in registred networks in show ip bgp table """
  client = MongoClient(config['mongo_server'], config['mongo_port'])
  db = client.stats
  collection = db.bgp_info

  first_digits = entrance.split('.')[0]
  regex = re.compile(first_digits, re.IGNORECASE)

  resultSet = []
  for result in collection.find({"Network": regex }) :
    resultSet.append(result)

  address = ipaddress.ip_address(u'%s'%entrance)
  checked_networks = {}
  for result in resultSet:
    value = address in ipaddress.ip_network(u'%s'%result['Network'])
    checked_networks[result['Network']] = value

  return checked_networks

def get_interfaces(network):
  """ Gets the tested network and connects to the router making an show ip route to this. After that, gets the interface of the matching networks """
  command = "sudo vtysh -c 'show ip route %s'" % network
  ssh = Ssh()
  util = Util()

  connection = ssh.connect(host=config['host'], username=config['username'], password=config['password'], timeout=config['timeout'])
  resultSet, stderr = ssh.sudoExecute(connection, command, config['password'])
  connection.close()
  print util.getting_interface(resultSet)

if __name__ == '__main__':
  all_networks = execute(sys.argv[1])
  possible_networks = [key for (key,value) in all_networks.items() if value == True]
  for network in possible_networks:
    get_interfaces(network)
