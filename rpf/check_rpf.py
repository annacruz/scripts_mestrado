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
  hosts    = config['hosts']
  username = config['username']
  password = config['password']
  timeout  = config['timeout']

  command = "sudo vtysh -c 'show ip route %s'" % network

  ssh  = Ssh()
  util = Util()

  possible_interfaces = []
  for host in hosts:
    connection = ssh.connect(host=host, username=username, password=password, timeout=timeout)
    resultSet, stderr = ssh.sudoExecute(connection, command, config['password'])
    connection.close()
    possible_interfaces.append(util.getting_interface(resultSet))

  return possible_interfaces

def check_rpf(ip_interface, possible_interfaces):
  if ip_interface in possible_interfaces:
    print 'Passed in Check RPF'
  else
    print 'Failed in Check RPF'


if __name__ == '__main__':
  all_networks = execute(sys.argv[1])
  possible_networks = [key for (key,value) in all_networks.items() if value == True]
  possible_interfaces = []
  for network in possible_networks:
    possible_interfaces = get_interfaces(network)
  check_rpf(sys.argv[2], possible_interfaces)
