#!/usr/bin/env python
from logging import debug, info, warning, error, exception, critical
from pprint import pprint, pformat

import aoc

def main(args):
	line_count = 0
	lines = []
	for line in args.input:
		line_count += 1
		lines.append(line)
	debug(f'Lines: {pformat(lines)}')
	info(f'Result: 17')

if __name__ == '__main__':
	parser = aoc.get_argparser()
	# Add problem-specifc args here
	args = aoc.parse_args(parser)
	
	main(args)