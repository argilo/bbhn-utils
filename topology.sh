#!/usr/bin/env bash

# Copyright 2014-2018 Clayton Smith
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

/home/pi/bbhn-utils/topology.py > /tmp/topology.dot
dot -Tpng -Ncolor=grey -Nstyle=filled -Nfillcolor=white -Nfontcolor=red -Nwidth=1 -Nfontsize=10 -Efontsize=10 -Gbgcolor=grey /tmp/topology.dot -o /tmp/topology.png
convert /tmp/topology.png -background \#C0C0C0 label:"`date`" -gravity East -append /tmp/topology2.png
cp /tmp/topology2.png /var/www/html/topology.png
aws s3 cp --acl public-read --cache-control max-age=60 /var/www/html/topology.png s3://media.ve3irr.ca/bbhn/topology.png
