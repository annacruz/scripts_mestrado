#!/usr/bin/env python
# coding=utf-8

from __future__ import with_statement
from sys import argv
from glob import glob
import re


files = glob(argv[1] + '/*')
files.sort()


ip_re = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')


for file in files	:
	with open(file) as f:
		first_line = f.readline().strip()
		if not ip_re.match(first_line):
			print '[ ! ] ' + file


