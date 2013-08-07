#! /usr/bin/env python
from pymongo import MongoClient
import re
import ipaddress

client = MongoClient('localhost', 27017)
db = client.stats
collection = db.bgp_info

entrance = '172.31.4.110'

first_digits = entrance.split('.')[0]
regex = re.compile(first_digits, re.IGNORECASE)

resultSet = []
for result in collection.find({"Network": regex }) : 
  resultSet.append(result)

address = ipaddress.ip_address(u'%s'%entrance)
for result in resultSet:
  print address in ipaddress.ip_network(u'%s'%result['Network'])
