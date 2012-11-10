#!/usr/bin/python

#
#   Copyright 2012 Dirk Zimmermann
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import Image
import argparse
import re
from pprint import pprint

class Point:
	"""A simple class for Points"""
	x = 0
	y = 0
	
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "Point ({0}, {1})".format(self.x, self.y)

def next_point(p, tilesize, maxsize):
	p.x = p.x + tilesize[0]
	if p.x > maxsize[0] - tilesize[0]:
		p.x = 0
		p.y = p.y + tilesize[1]
	return p

def retile(srcfile, destfile, tilesize, destsize):
	src = Image.open(srcfile) # src image
	dest = Image.new("RGB", destsize, None)
	srcp = Point(0,0) # src rectangle point (upper left)
	destp = Point(0,0) # dest rectangle point (upper left)
	while srcp.y < src.size[1] - tilesize[1]:
		box = (srcp.x, srcp.y, srcp.x + tilesize[0], srcp.y + tilesize[1])
		tile = src.crop(box)
		dest.paste(tile, (destp.x, destp.y))
		srcp = next_point(srcp, tilesize, src.size)
		destp = next_point(destp, tilesize, destsize)
	dest.save(destfile)

parser = argparse.ArgumentParser(description = 'Re-orders tiles in PNG files')
parser.add_argument('--in', metavar = 'input file', required = True, dest = 'infile', help = 'input PNG file')
parser.add_argument('--out', metavar = 'output file', required = True, help = 'output PNG file')
parser.add_argument('--tilesize', metavar = 'tilesize', required = True, help = 'tilesize (e.g. 16x16)')
parser.add_argument('--outsize', metavar = 'image size', required = True,
	help = 'size of the resulting image (e.g. 512x512)')

args = parser.parse_args();

size_matcher = re.compile(r"(\d+)x(\d+)")
m = size_matcher.match(args.tilesize)
tilesize = (int(m.group(1)), int(m.group(2)))
m = size_matcher.match(args.outsize)
outsize = (int(m.group(1)), int(m.group(2)))
retile(args.infile, args.out, tilesize, outsize)

