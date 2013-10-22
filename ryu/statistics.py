#! /usr/bin/env python

import time
import logging

from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.tests.integrated import tester

LOG = logging.getLogger(__name__)

class Statistics(tester.TestFlowBase):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(RunTest, self).__init__(*args, **kwargs)

        self._verify = None
        self.n_tables = ofproto_v1_3.OFPTT_MAX
        
    def run_verify(self, ev):
        msg = ev.msg
        dp = msg.datapath

        verify_func = self.verify_default
        v = "verify" + self.current[4:]
        if v in dir(self):
            verify_func = getattr(self, v)

        result = verify_func(dp, msg)
        if result is True:
            self.unclear -= 1

        self.results[self.current] = result
        self.start_next_test(dp)
        
    def verify_default(self, dp, msg):
        type_ = self._verify

        if msg.msg_type == dp.ofproto.OFPT_STATS_REPLY:
            return self.verify_stats(dp, msg.body, type_)
        elif msg.msg_type == type_:
            return True
        else:
            return 'Reply msg_type %s expected %s' \
                   % (msg.msg_type, type_)
            
    def verify_stats(self, dp, stats, type_):
        stats_types = dp.ofproto_parser.OFPStatsReply._STATS_TYPES
        expect = stats_types.get(type_).__name__

        if isinstance(stats, list):
            for s in stats:
                if expect == s.__class__.__name__:
                    return True
        else:
            if expect == stats.__class__.__name__:
                return True
        return 'Reply msg has not \'%s\' class.\n%s' % (expect, stats)
    
    def mod_flow(self, dp, cookie=0, cookie_mask=0, table_id=0,
                 command=None, idle_timeout=0, hard_timeout=0,
                 priority=0xff, buffer_id=0xffffffff, match=None,
                 actions=None, inst_type=None, out_port=None,
                 out_group=None, flags=0, inst=None):

        if command is None:
            command = dp.ofproto.OFPFC_ADD

        if inst is None:
            if inst_type is None:
                inst_type = dp.ofproto.OFPIT_APPLY_ACTIONS

            inst = []
            if actions is not None:
                inst = [dp.ofproto_parser.OFPInstructionActions(
                        inst_type, actions)]

        if match is None:
            match = dp.ofproto_parser.OFPMatch()

        if out_port is None:
            out_port = dp.ofproto.OFPP_ANY

        if out_group is None:
            out_group = dp.ofproto.OFPG_ANY

        m = dp.ofproto_parser.OFPFlowMod(dp, cookie, cookie_mask,
                                         table_id, command,
                                         idle_timeout, hard_timeout,
                                         priority, buffer_id,
                                         out_port, out_group,
                                         flags, match, inst)

        dp.send_msg(m)
        
    #def test_flow_add_goto_table(self, dp):
    #    self._verify = dp.ofproto.OFPIT_GOTO_TABLE
    #
    #    inst = [dp.ofproto_parser.OFPInstructionGotoTable(0), ]
    #    self.mod_flow(dp, inst=inst)
    #    self.send_flow_stats(dp)

    
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        if self.current.find('packet_in'):
            self.run_verify(ev)
