#!/usr/bin/env python

import sys, time
from daemon import Daemon
from ssh_connection_util import Ssh
from bgp_table_util import Util
from pymongo import MongoClient
import json

class BgpInfo(Daemon):
  global config
  config = json.load(open("config/config.cfg"))

  def run(self):
    while True:
      get_bgp_info()
      time.sleep(30)

  def get_bgp_info(self):
    hosts     = config['host']
    username  = config['username']
    password  = config['password']
    timeout   = config['timeout']
    command   = "sudo vtysh -c 'show ip bgp'"

    client     = MongoClient('localhost', 27017)
    db         = client.stats
    db.bgp_info.drop()
    collection = db.bgp_info


    ssh  = Ssh()
    util = Util()

    for host in hosts:
      connection = ssh.connect(host=host, username=username, password=password, timeout=timeout)
      resultSet, stderr = ssh.sudoExecute(connection, command, password)
      connection.close()
      bgpDict = util.convert_to_dict(resultSet, host)
      print bgpDict
      collection.insert(bgpDict)

if __name__ == "__main__":
  daemon = BgpInfo('/tmp/bgpinfo.pid')
  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      daemon.start()
    elif 'stop' == sys.argv[1]:
      daemon.stop()
    elif 'restart' == sys.argv[1]:
      daemon.restart()
    else:
      print "Unknown command"
      sys.exit(2)
    sys.exit(0)
  else:
    print "usage: %s start|stop|restart" % sys.argv[0]
    sys.exit(2)
