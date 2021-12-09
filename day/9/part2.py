#!/usr/bin/env python
from functools import reduce
from logging import debug, info, warning, error, exception, critical
from pprint import pprint, pformat

import aoc

class Map:
	def __init__(self, map):
		cols = len(map[0])
		assert all(len(row) == cols for row in map)
		self.map = map
		debug(f'Floor rows: {self.rows}')
		debug(f'Floor cols: {self.cols}')
	
	@property
	def cols(self):
		return len(self.map[0])
	
	@property
	def rows(self):
		return len(self.map)
	
	def height(self, row, col):
		return self.map[row][col]
	
	def neighbors(self, row, col):
		if row > 0:
			yield row-1, col
		if col < self.cols - 1:
			yield row, col+1
		if row < self.rows - 1:
			yield row+1, col
		if col > 0:
			yield row, col-1

def find_basin(map, low_point):
	# debug(f'Finding basin for {low_point}')
	basin = set()
	to_search = [low_point]
	marked = {low_point}
	while to_search:
		# debug(f'Queue length: {len(to_search)}')
		candidate = to_search.pop()
		# debug(f'Considering {candidate}')
		if map.height(*candidate) == 9:
			# debug(f'Candidate height 9; discarding')
			continue
		# debug('Adding to basin')
		basin.add(candidate)
		for neighbor in map.neighbors(*candidate):
			if neighbor not in marked:
				# debug(f'Marking {neighbor} and adding to search queue')
				to_search.append(neighbor)
				marked.add(neighbor)
	debug(f"Found basin: {pformat(basin)}")
	return frozenset(basin)

def main(args):
	map = Map([[int(c) for c in line if c != '\n'] for line in args.input])
	basins = set()
	for row in range(map.rows):
		for col in range(map.cols):
			height = map.height(row, col)
			if all(height < map.height(*neighbor) for neighbor in map.neighbors(row, col)):
				basin = find_basin(map, (row, col))
				debug(f'Position {row, col} is a low point with basin size {len(basin)}')
				basins.add(basin)
	
	debug(f'All basins: {pformat(basins)}')
	three_largest = sorted(basins, key=len, reverse=True)[:3]
	debug(f'Three largest basins: {pformat(three_largest)}')
	info(f'Largest basin product: {reduce(lambda x,y: x*y, (len(basin) for basin in three_largest))}')

if __name__ == '__main__':
	parser = aoc.get_argparser()
	# Add problem-specifc args here
	args = aoc.parse_args(parser)
	
	main(args)