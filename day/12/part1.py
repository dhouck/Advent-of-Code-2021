#!/usr/bin/env python
from collections import defaultdict
from dataclasses import dataclass
from logging import debug, info, warning, error, exception, critical
from pprint import pprint, pformat

import aoc

@dataclass(slots=True, frozen=True)
class Node:
	name: str
	
	@property
	def big(self) -> bool:
		return self.name.isupper()

def DFS(nodes, start=Node('start'), goal=Node('end'), seen=None):
	if seen is None:
		seen = {start}
	
	if start == goal:
		yield [start]
	else:
		for node in nodes[start]:
			if node in seen and not node.big:
				continue
			
			for path in DFS(nodes, node, goal, seen | {node}):
				yield [start] + path

def main(args):
	nodes = defaultdict(set)
	for line in args.input:
		first, second = line.strip().split('-')
		nodes[Node(first)].add(Node(second))
		nodes[Node(second)].add(Node(first))
	info(f'Loaded graph with {len(nodes)} nodes')
	debug(pformat(nodes))
	
	count = 0
	for path in DFS(nodes):
		debug(f'Found path: {path}')
		count += 1
	info(f'There were {count} paths')

if __name__ == '__main__':
	parser = aoc.get_argparser()
	# Add problem-specifc args here
	args = aoc.parse_args(parser)
	
	main(args)