#!/usr/bin/python
# Author: Anna Cruz <anna.cruz@uniriotec.br>
#
# This file is a script to be used as POX module.
#
#

"""
This script collects flow informations on all switches connected
in this instance of POX.
"""

from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from pox.openflow.of_json import *
from pymongo import MongoClient
from datetime import datetime
import time

log = core.getLogger()
client = MongoClient('localhost', 27017)
db = client.pox_stats
flow_collection = db.flow_collection

def _timer_func():
  for connection in core.openflow._connections.values():
    connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
    connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
  log.info("Sent %i flow/port stats request(s)", len(core.openflow._connections))

def _handle_flowstats_received(event):
  # dp_id = dpidToStr(event.connection.dpid)
  # flow = create_flow_stats_list(event.stats)
  # if len(flow) != 0:
  #   flow_dict = dict((key,value) for key,value in flow[0].items())
  #   dt = datetime.now()
  #   now = time.mktime(dt.timetuple())
  #   flow_dict['time'] = now
  #   flow_dict['dp_id'] = dp_id
  #   flow_dict.pop('match', None)
  #   flow_collection.insert(flow_dict)
  #   log.info("%s",  flow_dict)
  web_bytes = 0
  web_flows = 0
  for f in event.stats:
    if f.match.tp_dst == 80 or f.match.tp_src == 80:
      web_bytes += f.byte_count
      web_flows += 1
  log.info("WEB TRAFFIC: %s ----------- %s" % web_bytes, web_flows)

def create_flow_stats_list(flows):
  flowlist = []
  for flow in flows:
      flowlist.append({
      "length": len(flow),
      "table_id": flow.table_id,
      "stats": create_match_dict(flow.match),
      "duration_sec": flow.duration_sec,
      "duration_nsec": flow.duration_nsec,
      "priority": flow.priority,
      "idle_timeout": flow.idle_timeout,
      "hard_timeout": flow.hard_timeout,
      "cookie": flow.cookie,
      "packet_count": flow.packet_count,
      "byte_count": flow.byte_count,
      })
  return flowlist

def create_match_dict(match):
  # TODO: do this properly and not depending on POX behavior
  match = match.show().strip("\n").split("\n")
  print match
  result = dict([attr.split(": ") for attr in match])
  print result
  try:
      w = result["wildcards"]
      p = w[w.find("nw_dst"):]
      s = p.find("(") + 2 # Strip (/
      e = p.find(")")
      netmask = int(p[s:e])
  except:
      netmask = 0
  if netmask != 0 and "nw_dst" in result:
      result["nw_dst"] = result["nw_dst"] + "/" + str(netmask)
  return result

# main functiont to launch the module
def launch():
  from pox.lib.recoco import Timer

  # attach handsers to listners
  core.openflow.addListenerByName(
      "FlowStatsReceived",
      _handle_flowstats_received)

  Timer(5, _timer_func, recurring=True)

