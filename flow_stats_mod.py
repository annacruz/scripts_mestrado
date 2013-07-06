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
def _handle_flowstats_received (event):
  flows_stats = flow_stats_to_list(event.stats)
  to_collection = {}
  if len(flows_stats) != 0:
    for brute_flow in flows_stats:
      flow = transform_to_dict(brute_flow)
      #log.info(flow['priority'])
      flow_collection.insert(flow['priority'])

#    log.info("FlowStatsReceived from %s: %s || %s",
#    dpidToStr(event.connection.dpid), flows_stats, flow['match']['in_port'])
    log.info("%s", flow['match']['in_port'])
  
  #log.info("FlowStatsReceived from %s: %s ",
  #dpidToStr(event.connection.dpid), flows_stats )


def transform_to_dict(data):
  return dict((key,value) for key,value in data.iteritems())

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

