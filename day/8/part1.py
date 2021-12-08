#!/usr/bin/env python

import fileinput

def parse_line(line):
	samples, data = line.split('|')
	return samples.split(), data.split()

count = 0
for line in fileinput.input():
	samples, data = parse_line(line)
	for digit in data:
		if len(digit) in {2, 3, 4, 7}:
			count += 1

print(count)