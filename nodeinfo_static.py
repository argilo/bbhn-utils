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

from jinja2 import Environment, PackageLoader
import json
from datetime import *
import os
from node_db import NodeDB

DISPLAY_HOURS = 24
OUTPUT_DIR = 'html_out'


def mkdir(d):
    if not os.path.exists(d):
        os.makedirs(d)

env = Environment(
    loader=PackageLoader('nodeinfo_static', 'templates'),
    autoescape=True
)

node_db = NodeDB()

last_seen = node_db.last_seen(DISPLAY_HOURS)
template = env.get_template('index.html')
mkdir(OUTPUT_DIR)
with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w') as f:
    f.write(template.render(last_seen=last_seen))

template = env.get_template('link.html')
for node in last_seen:
    ip = node[0]
    name = node_db.name(ip)
    neighbours = node_db.neighbours(ip, DISPLAY_HOURS)

    for neighbour in neighbours:
        last_hop_ip = neighbour[1]
        cost = node_db.cost_history(ip, last_hop_ip, DISPLAY_HOURS)

        cost = [(int(ts.timestamp() * 1000), lq) for ts, lq in cost]
        dest_dir = os.path.join(OUTPUT_DIR, 'linkdata', ip)
        mkdir(dest_dir)
        with open(os.path.join(dest_dir, last_hop_ip + '.json'), 'w') as f:
            f.write(json.dumps(cost, separators=(',', ':')))

    dest_dir = os.path.join(OUTPUT_DIR, 'link')
    mkdir(dest_dir)
    with open(os.path.join(dest_dir, ip + '.html'), 'w') as f:
        f.write(template.render(ip=ip, name=name, neighbours=neighbours))

node_db.close()
