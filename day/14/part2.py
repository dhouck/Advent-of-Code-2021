#!/usr/bin/env python
import collections
import itertools
from logging import debug, info, warning, error, exception, critical
from pprint import pprint, pformat

import aoc

def advance(digraphs, insertions):
	debug(f'Building successor to {digraphs}')
	new_digraphs = collections.Counter()
	for digraph, count in digraphs.items():
		if digraph in insertions:
			first, third = digraph
			second = insertions[digraph]
			new_digraphs[first+second] += count
			new_digraphs[second+third] += count
		else:
			new_digraphs[digraph] += count
	return new_digraphs

def make_digraphs(polymer):
	return collections.Counter(''.join(pair) for pair in itertools.pairwise(polymer))

def count_elements(digraphs, last):
	elem_counts = collections.Counter()
	for digraph, count in digraphs.items():
		elem_counts[digraph[0]] += count
	elem_counts[last] += 1
	return elem_counts

def main(args):
	polymer = args.input.readline().strip()
	digraphs = make_digraphs(polymer)
	
	args.input.readline() # Blank
	
	insertions = dict(line.strip().split(' -> ') for line in args.input)
	debug(f'List of insertions:\n{pformat(insertions)}')
	for i in range(1, args.steps + 1):
		digraphs = advance(digraphs, insertions)
		debug(f'After round {i}, digraphs are {digraphs}')
	counts = count_elements(digraphs, polymer[-1])
	info(f'Final element counts: {counts}')
	print(f'Score: {max(counts.values()) - min(counts.values())}')

if __name__ == '__main__':
	parser = aoc.get_argparser()
	parser.add_argument('-s', '--steps', default=10, type=int)
	# Add problem-specifc args here
	args = aoc.parse_args(parser)
	
	main(args)