#!/usr/bin/python

import subprocess
import re
import sys

'''
spitefulgrog - Spirit Scripts
'''


process = subprocess.Popen(['sudo', 'unbound-control', 'stats'], stdout=subprocess.PIPE)

stats = {}

while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
                break
        if output:
                if re.search('thread.', output.strip()) or re.search('total.', output.strip()):
                        newthread = output.strip().split('.')[0]
                        if not newthread in stats:
                                stats.update({newthread : []})
                if re.search('.num.queries.', output.strip()):
                        queries = output.strip().split('=')[-1]
                        thread = output.strip().split('.')[0]
                        stats[thread].insert(0, queries)
                elif re.search('.num.cachehits.', output.strip()):
                        cachehits = output.strip().split('=')[-1]
                        thread = output.strip().split('.')[0]
                        stats[thread].insert(1, cachehits)
                elif re.search('.num.cachemiss.', output.strip()):
                        cachemiss = output.strip().split('=')[-1]
                        thread = output.strip().split('.')[0]
                        stats[thread].insert(2, cachemiss)

output = "Stats stored"
perfdata = "| "
index = len(stats) - 1
perfdata = perfdata + "index=" + str(index) + " "
for key, value in stats.iteritems():
        perfdata =  perfdata + str(key) + "_queries" + "=" + str(value[0]) + " " + str(key) + "_cachehits" + "=" + str(value[1]) + " " \
                + str(key) + "_cachemiss" + "=" + str(value[2]) + " "

print output + perfdata
sys.exit(0)
