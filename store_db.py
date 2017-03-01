#!/usr/bin/env python3

# Copyright 2017 Clayton Smith
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
import datetime
import psycopg2

HOST = "localnode"
PORT = 2006


def getTable(lines, tableName):
    lines = lines[lines.index("Table: " + tableName) + 2:]
    lines = lines[:lines.index("")]
    return [line.split("\t") for line in lines]


def getHost(ip):
    try:
        host = socket.gethostbyaddr(ip)[0]
        return host.replace(".local.mesh", "")
    except socket.herror:
        return ip


lines = urllib.request.urlopen("http://" + HOST + ":" + str(PORT) +
                               "/").readlines()
lines = [line.decode().strip() for line in lines]

topology = getTable(lines, "Topology")

timestamp = datetime.datetime.now()
conn = psycopg2.connect("dbname=topology")
cur = conn.cursor()
for t in topology:
    t.append(getHost(t[0]))
    t.append(getHost(t[1]))
    cur.execute("""INSERT INTO topology
        (time, dest_ip, dest_name, last_hop_ip, last_hop_name, lq, nlq, cost)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (timestamp, t[0], t[5], t[1], t[6], t[2], t[3],
        "Infinity" if t[4] == "INFINITE" else t[4]))
conn.commit()
cur.close()
conn.close()
