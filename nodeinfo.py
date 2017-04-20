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

from flask import Flask, render_template, Response
import json
from datetime import *
from node_db import NodeDB

DISPLAY_HOURS = 24

node_db = NodeDB()
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def node_info():
    last_seen = node_db.last_seen(DISPLAY_HOURS)
    return render_template('index.html', last_seen=last_seen)

@app.route('/link/<ip>.html')
def link_info(ip):
    name = node_db.name(ip)
    neighbours = node_db.neighbours(ip, DISPLAY_HOURS)
    return render_template('link.html', ip=ip, name=name, neighbours=neighbours)

@app.route('/linkdata/<dest_ip>/<last_hop_ip>.json')
def link_data(dest_ip, last_hop_ip):
    cost = node_db.cost_history(dest_ip, last_hop_ip, DISPLAY_HOURS)
    cost = [(ts.timestamp() * 1000, lq) for ts, lq in cost]
    return Response(json.dumps(cost), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    node_db.close()
