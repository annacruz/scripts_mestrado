#!/usr/bin/python
# Author: Anna Cruz <anna.cruz@uniriotec.br>
#
# This file is a script to be used as POX module.
#
# POX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# POX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with POX. If not, see <http://www.gnu.org/licenses/>.
#

"""
This script collects flow informations on all switches connected
in this instance of POX.
"""

# standard includes
from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from pox.openflow.of_json import *
from pymongo import MongoClient

log = core.getLogger()
client = MongoClient('localhost', 27017)
db = client.pox_stats
flow_collection = db.flow_collection


# handler for timer function that sends the requests to all the
# switches connected to the controller.
def _timer_func():
  for connection in core.openflow._connections.values():
    connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
    connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
  log.info("Sent %i flow/port stats request(s)", len(core.openflow._connections))

# handler to display flow statistics received in JSON format
# structure of event.stats is defined by ofp_flow_stats()
# def _handle_flowstats_received (event):
#   flows_stats = flow_stats_to_list(event.stats)
#   to_collection = {}
#   if len(flows_stats) != 0:
#     for brute_flow in flows_stats:
#       flow = transform_to_dict(brute_flow)
      #log.info(flow['priority'])
      # flow_collection.insert(flow['priority'])

#    log.info("FlowStatsReceived from %s: %s || %s",
#    dpidToStr(event.connection.dpid), flows_stats, flow['match']['in_port'])
    # log.info("%s", flow['match']['in_port'])

  #log.info("FlowStatsReceived from %s: %s ",
  #dpidToStr(event.connection.dpid), flows_stats )

def _handle_flowstats_received(event):
  dp_id = event.connection.dpid
  flow = create_flow_stats_list(event.stats)
  flow_dict = dict((key,value) for key,value in flow.iteritems())
  flow_collection.update(dp_id, "switch", flows=flow_dict)

def create_flow_stats_list(flows):
  flowlist = []
  for flow in flows:
      flowlist.append({
      "length": len(flow),
      "table_id": flow.table_id,
      "match": create_match_dict(flow.match),
      "duration_sec": flow.duration_sec,
      "duration_nsec": flow.duration_nsec,
      "priority": flow.priority,
      "idle_timeout": flow.idle_timeout,
      "hard_timeout": flow.hard_timeout,
      "cookie": flow.cookie,
      "packet_count": flow.packet_count,
      "byte_count": flow.byte_count,
      "actions": create_actions_list(flow.actions),
      })
  return flowlist

def create_match_dict(match):
  # TODO: do this properly and not depending on POX behavior
  match = match.show().strip("\n").split("\n")
  result = dict([attr.split(": ") for attr in match])
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

def create_aggregate_stats_dict(aggregate):
  return {
  "packet_count": aggregate.packet_count,
  "byte_count": aggregate.byte_count,
  "flow_count": aggregate.flow_count,
  }

def create_actions_list(actions):
# TODO: do this properly and not depending on POX behavior
  actionlist = []
  for action in actions:
    string = action.__class__.__name__ + "["
    string += action.show().strip("\n").replace("\n", ", ") + "]"
    actionlist.append(string)
  return actionlist

def _handle_portstats_received (event):
  stats = flow_stats_to_list(event.stats)
  log.info("PortStatsReceived from %s: %s",
    dpidToStr(event.connection.dpid), stats)

# main functiont to launch the module
def launch():
  from pox.lib.recoco import Timer

  # attach handsers to listners
  core.openflow.addListenerByName(
      "FlowStatsReceived",
      _handle_flowstats_received)
  #core.openflow.addListenerByName(
  #    "PortStatsReceived",
  #    _handle_portstats_received)

  # timer set to execute every five seconds
  Timer(5, _timer_func, recurring=True)

