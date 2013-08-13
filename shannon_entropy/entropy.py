#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time 

#sys.path.append('/Users/alex/Mestrado/anomaly/bin/new/lib')
sys.path.append('/home/yui/dev/mestrado/code/lib')

from flows.utils      import Configuration
from flows.utils      import progressbar
from flows.entropy    import Entropy
from flows.algorithms import createrrd
import flows.algorithms

# configuration loading
if len(sys.argv) == 2:
  configuration_file =  sys.argv[1] 
else: 
  configuration_file = 'flows2.ini'

configuration = Configuration(configuration_file)

# creating EWMA RRD files #EWMA
#ewma_files = [ "sa-ewma.rrd", "sp-ewma.rrd","dp-ewma.rrd", "da-ewma.rrd" ] # EWMA
#for rrd_file_ewma in ewma_files: #EWMA
#    if not os.path.isfile(rrd_file_ewma): #EWMA
#        createrrd(rrd_file_ewma, '200801010000') #EWMA

# samples directory
directory = configuration.data['entropy']['samples']

# mapping 'type' to its RRDTools file
types = {}

types_list = configuration.data['entropy']['types']

for type in types_list.split(','):
	type_key, type_value = type.split(':')
	types[type_key.strip()] = type_value.strip() 

# algorithm
algorithm_name = configuration.data['entropy']['algorithm'].lower()
algorithm = eval('flows.algorithms.%s' % (algorithm_name))

# evaluating Entropy from the information in the configuration file: flows.ini by default
for type, file in types.iteritems():
	e = Entropy(directory, '*%s*' % type)
	e.evaluate(algorithm, file)
