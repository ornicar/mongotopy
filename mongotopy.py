#! /usr/bin/env python3
import os
import subprocess
import json

seconds = '10'
filename = "mongodataforlukhas"

def reformat(data):
    formatted = []
    data = data['totals']
    for dbcoll in data:
        database, coll = dbcoll.split(".",1)
        for op in ["read", "write"]:
            for field in ["time", "count"]:
                formatted.append('"database":"{}", "coll":"{}", "op":"{}", "field": "{}", "value":{}'.format(database, coll, op, field, data[dbcoll][op][field]))
    return "\n".join(formatted)

def saveMongoData():
    mongocall = subprocess.Popen(['mongotop', '--json', '--rowcount=1', seconds], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = mongocall.communicate()
    mongodata = reformat(json.loads(stdout.decode("utf-8")))
    with open('tmpFile', 'w') as f:
        f.write(mongodata)
    os.rename('tmpFile', filename)

while True:
    saveMongoData()
