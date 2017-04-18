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

from flask import Flask, render_template, request, Response
import json
import psycopg2
from datetime import *

DISPLAY_HOURS = 24

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def node_info():
    conn = psycopg2.connect("dbname=topology")
    cur = conn.cursor()
    cur.execute("""SELECT dest_ip, dest_name, ts,
        ts > NOW() - INTERVAL '%s hours'
        FROM last_seen
        ORDER BY dest_name""", (DISPLAY_HOURS,))
    last_seen = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('index.html', last_seen=last_seen)

@app.route('/link/<ip>.html')
def link_info(ip):
    conn = psycopg2.connect("dbname=topology")
    cur = conn.cursor()
    name = fetch_name(cur, ip)
    cur.execute("""SELECT DISTINCT last_hop_ip FROM topology
        WHERE ts > NOW() - INTERVAL '%s hours'
        AND dest_ip=%s
        ORDER BY last_hop_ip""", (DISPLAY_HOURS, ip))
    neighbours = cur.fetchall()

    for i, neighbour in enumerate(neighbours):
        neighbours[i] = (i,) + neighbour + (fetch_name(cur, neighbour[0]),)
    cur.close()
    conn.close()

    return render_template('link.html', ip=ip, name=name, neighbours=neighbours)

@app.route('/linkdata/<dest_ip>/<last_hop_ip>.json')
def link_data(dest_ip, last_hop_ip):
    conn = psycopg2.connect("dbname=topology")
    cur = conn.cursor()
    now = datetime.now()
    cur.execute("""SELECT ts, lq * nlq FROM topology
        WHERE ts > NOW() - INTERVAL '%s hours'
        AND dest_ip=%s
        AND last_hop_ip=%s
        ORDER BY ts""", (DISPLAY_HOURS, dest_ip, last_hop_ip))
    cost = []
    last_time = now - timedelta(hours=DISPLAY_HOURS)
    for row in cur:
        interval_min = round((row[0] - last_time).total_seconds() / 60)
        if interval_min >= 2:
            cost.append((last_time + timedelta(minutes=1), 0))
        if interval_min >= 3:
            cost.append((row[0] - timedelta(minutes=1), 0))
        cost.append(row)
        last_time = row[0]
    interval_min = round((now - last_time).total_seconds() / 60)
    if interval_min >= 2:
        cost.append((last_time + timedelta(minutes=1), 0))
        cost.append((now, 0))
    cur.close()
    conn.close()

    cost = [(ts.timestamp() * 1000, lq) for ts, lq in cost]
    return Response(json.dumps(cost), mimetype='application/json')

def fetch_name(cur, ip):
    cur.execute("""SELECT dest_name FROM last_seen
        WHERE dest_ip=%s""", (ip,))
    result = cur.fetchone()
    if result[0]:
        return result[0]
    else:
        return ip

if __name__ == '__main__':
    app.run(host='0.0.0.0')
