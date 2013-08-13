# coding=UTF-8

import re
import sys

class Configuration:

  """
  Represents a '.ini'-like configuration file.
  """

  def __init__(self, file):

    self.file = file
    self.data = {}

    self.__parse()


  def __parse(self):
    
    regexp_section = re.compile(
        '^[\s]*'              # any number of 'white space' character
        '\['                  # literal '[' 
        '(?P<section>[^\]]+)' # section name
        ' \]'                 # literal ']'
        , re.VERBOSE | re.IGNORECASE
    )

    regexp_key_value = re.compile(
        '(?P<key>^[^=]+)'      # key (any group of characters not including '=')
        '\s*=\s*'              # literal '=' surrounded by any number of space characters 
        '(?P<value>.+)'     # value (any group of characters not including '=')
        , re.VERBOSE | re.IGNORECASE
    )

    section = None

    for line in open(self.file):
      line = line.strip()
      if len(line) > 0 and not line.startswith('#'):
        match_section = regexp_section.match(line)
        match_key_value = regexp_key_value.match(line)
        if match_section:
          section = match_section.group('section')
          self.data[section] = {}
        elif match_key_value:
          if section != None:
            self.data[section][match_key_value.group('key').strip()] = match_key_value.group('value').strip()  

class progressbar(object):
    def __init__(self, finalcount, block_char='.'):
        self.finalcount = finalcount
        self.blockcount = 0
        self.block = block_char
        self.f = sys.stdout
        if not self.finalcount: return
        self.f.write('\n------------------ % Progress -------------------1\n')
        self.f.write('    1    2    3    4    5    6    7    8    9    0\n')
        self.f.write('----0----0----0----0----0----0----0----0----0----0\n')
    def progress(self, count):
        count = min(count, self.finalcount)
        if self.finalcount:
            percentcomplete = int(round(100.0*count/self.finalcount))
            if percentcomplete < 1: percentcomplete = 1
        else:
            percentcomplete=100
        blockcount = int(percentcomplete//2)
        if blockcount <= self.blockcount:
            return
        for i in range(self.blockcount, blockcount):
            self.f.write(self.block)
        self.f.flush( )
        self.blockcount = blockcount
        if percentcomplete == 100:
            self.f.write("\n")
