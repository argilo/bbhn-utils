#!/usr/bin/python3

# Copyright 2014-2015 Clayton Smith
#
# This file is part of bbhn-utils
#
# bbhn-utils is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# bbhn-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with bbhn-utils; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

import urllib.request
import socket

HOST = "localnode"
PORT = 2006

def getTable(lines, tableName):
  lines = lines[lines.index("Table: " + tableName)+2:]
  lines = lines[:lines.index("")]
  return [line.split("\t") for line in lines]

def getHost(ip):
  try:
    host = socket.gethostbyaddr(ip)[0]
    return host.replace(".local.mesh", "").replace("-", "-\\n", 1)
  except socket.herror:
    return ip

def getCall(host):
  i = host.find("-")
  if i == -1: return host
  else: return host[:i].upper()

def roundCost(cost):
  if cost == "INFINITE":
    return cost
  else:
    cost = float(cost)
    return "{0:.1f}".format(cost)

def printLink(t):
  if t[4] == "0.100": # Ethernet connection
    print('    "' + t[6] + '" -> "' + t[5] + '" [dir=none, penwidth=3];')
  else:
    if t[4] == "INFINITE":
      darkness = 0.0
    else:
      darkness = 1.0 / float(t[4])
    gray = "gray" + str(int(65.0 * (1.0 - darkness)))
    print('    "' + t[6] + '" -> "' + t[5] + '" [label="' + roundCost(t[4]) + '",color=' + gray + ',fontcolor=' + gray + '];')

def pruneTopology(nodes, topology):
  ethernetSpanningForest = set()
  visited = set()
  for node, links in nodes.items():
    if node in visited: continue
    spanningTree = []
    toVisit = [(node, None)]
    while len(toVisit) > 0:
      currentNode, link = toVisit.pop()
      if currentNode in visited: continue
      visited.add(currentNode)
      if link:
        ethernetSpanningForest.add(tuple(link))
      for link in nodes[currentNode]:
        if link[4] == "0.100":
          toVisit.append((link[0], link))
  return [t for t in topology if t[4] != "0.100" or tuple(t) in ethernetSpanningForest]

lines = urllib.request.urlopen("http://" + HOST + ":" + str(PORT) + "/").readlines()
lines = [line.decode().strip() for line in lines]

topology = getTable(lines, "Topology")

# Look up DNS names of hosts and create node dictionary
nodes = {}
for t in topology:
  t.append(getHost(t[0]))
  t.append(getHost(t[1]))
  nodes.setdefault(t[1], []).append(t)

topology = pruneTopology(nodes, topology)

groups = {}
nongroups = []
for t in topology:
  dstCall = getCall(t[5])
  srcCall = getCall(t[6])
  if dstCall == srcCall:
    if dstCall in groups: groups[dstCall].append(t)
    else: groups[dstCall] = [t]
  else:
    nongroups.append(t)

print("digraph topology {")
for call, links in groups.items():
  print("  subgraph cluster_" + call + " {")
  print("    style=dotted;")
  for t in links:
    printLink(t)
  print("  }")
for t in nongroups:
  printLink(t)
print("}")
