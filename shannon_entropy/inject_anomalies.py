#!/usr/bin/env python
# coding=UTF-8

from __future__ import with_statement

import sys
sys.path.append('/home/yui/dev/mestrado/lib')

from flows.utils import Configuration
from flows.injector import Injector

# scale: Fator de escala a ser aplicado nos registros de anomalias. 
# Escalas usadas no paper para o SBRC 2009: 0.02919 (para 10%), 0.14595 (50%) e 0.5838 (20%)
# configuration loading

if len(sys.argv) == 2:
    configuration_file =  sys.argv[1] 
else: 
    configuration_file = 'flows2.ini'

configuration = Configuration(configuration_file)

# injection
injector = Injector(configuration.data['injection'])
injector.inject()

