#! /usr/bin/env python
from pymongo import MongoClient
import re
import sys
import ipaddress
import json

def execute(entrance):
  config = json.load(open("config/config.cfg"))
  client = MongoClient(config['mongo_server'], int(config['mongo_port']))
  db = client.stats
  collection = db.bgp_info

  first_digits = entrance.split('.')[0]
  regex = re.compile(first_digits, re.IGNORECASE)

  resultSet = []
  for result in collection.find({"Network": regex }) :
    resultSet.append(result)

  address = ipaddress.ip_address(u'%s'%entrance)
  checkedNetworks = {}
  for result in resultSet:
    value = address in ipaddress.ip_network(u'%s'%result['Network'])
    checkedNetworks[result['Network']] = value

  print checkedNetworks

if __name__ == '__main__':
  execute(sys.argv[1])
