from pox.core import core
from pox.lib.revent import Event
class FlowRemoved (Event):
  def __init__ (self, connection, ofp):
    Event.__init__(self)
    self.connection = connection
    self.dpid = connection.dpid
    self.ofp = ofp
    self.idleTimeout = False
    self.hardTimeout = False
    self.deleted = False
    self.timeout = False
    if ofp.reason == of.OFPRR_IDLE_TIMEOUT:
      self.timeout = True
      self.idleTimeout = True
      log.debug("In first if")
    elif ofp.reason == of.OFPRR_HARD_TIMEOUT:
      self.timeout = True
      self.hardTimeout = True
      log.debug("In second if")
    elif ofp.reason == of.OFPRR_DELETE:
      self.deleted = True
      log.debug("In third if")
