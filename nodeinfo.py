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

from flask import Flask
from flask import render_template
import psycopg2

app = Flask(__name__)

@app.route('/')
def node_info():
    conn = psycopg2.connect("dbname=topology")
    cur = conn.cursor()
    cur.execute("""SELECT dest_ip, dest_name, ts FROM last_seen
        ORDER BY dest_name""")
    last_seen = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', last_seen=last_seen)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
