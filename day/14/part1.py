#!/usr/bin/env python
import collections
import itertools
from logging import debug, info, warning, error, exception, critical
from pprint import pprint, pformat

import aoc

def advance(polymer, insertions):
	def generate_elements(polymer, insertions):
		for pair in itertools.pairwise(polymer):
			yield pair[0]
			if (insertion := insertions.get(''.join(pair))) is not None:
				yield insertion
		yield polymer[-1]
	debug(f'Building successor to {polymer}')
	return ''.join(generate_elements(polymer, insertions))

def main(args):
	polymer = args.input.readline().strip()
	args.input.readline() # Blank
	insertions = dict(line.strip().split(' -> ') for line in args.input)
	debug(f'List of insertions:\n{pformat(insertions)}')
	for i in range(1, args.steps + 1):
		polymer = advance(polymer, insertions)
		debug(f'After round {i}, polymer is {polymer}')
	counts = collections.Counter(polymer)
	info(f'Final element counts: {counts}')
	print(f'Score: {max(counts.values()) - min(counts.values())}')

if __name__ == '__main__':
	parser = aoc.get_argparser()
	parser.add_argument('-s', '--steps', default=10, type=int)
	# Add problem-specifc args here
	args = aoc.parse_args(parser)
	
	main(args)