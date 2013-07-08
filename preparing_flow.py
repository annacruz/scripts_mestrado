#!/usr/bin/python

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.pox_stats
flow_collection = db.flow_collection

flow = flow_collection.aggregate({"$group" : { "_id": "$stats.nw_src", "total_packets": { "$sum" : "$packet_count"}}})

print flow
