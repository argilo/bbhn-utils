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

import psycopg2

conn = psycopg2.connect("dbname=topology")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE topology (
        time timestamp,
        dest_ip inet,
        dest_name varchar,
        last_hop_ip inet,
        last_hop_name varchar,
        lq real,
        nlq real,
        cost real,
        PRIMARY KEY(time, dest_ip, last_hop_ip)
    );
""")
conn.commit()
cur.close()
conn.close()
