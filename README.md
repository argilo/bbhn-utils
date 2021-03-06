```
# Copyright 2014-2016 Clayton Smith
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
```

bbhn-utils
==========

Author: Clayton Smith (VE3IRR)  
Email: <argilo@gmail.com>

This repository contains utilities that may be of interest to operators
of Broadband-Hamnet nodes. For information about Broadband-Hamnet,
refer to http://www.broadband-hamnet.org/.

The first utility is a Python script (topology.py) that generates mesh
topology diagrams.  Sample output can be seen here:

http://ve2zaz.net/BBHN-Ottawa_www/

Each mesh node appears in an oval. Arrows between nodes indicate the
link cost (i.e. expected number of transmissions required per packet).
Solid lines between nodes indicate Ethernet links. Nodes beginning with
the same call sign are grouped together.

The Python script connects to a mesh node on port 2006 to fetch
topology data, then produces a Graphviz DOT file as output. A sample
shell script (topology.sh) demonstrates how to convert the resulting
DOT file to a PNG image. It also adds the current UTC time to the PNG
using ImageMagick and publishes the result to local web server and an
Amazon S3 bucket.

Requirements:

* Python 3
* Graphviz
* ImageMagick (optional)
* Amazon AWS CLI (optional)
