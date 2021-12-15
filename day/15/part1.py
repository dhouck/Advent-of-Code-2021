#!/usr/bin/env python
from __future__ import annotations

import itertools

from dataclasses import dataclass
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
	
	def __getitem__(self, cell):
		return self.map[cell[0]][cell[1]]
	
	def __setitem__(self, key, value):
		# debug(f'Assigning {value} to {key}')
		row, col = key
		self.map[row][col] = value
	# debug(f'Position {key} is now {self[key]} == {self.map[row][col]}')
	
	def __iter__(self):
		return itertools.product(range(self.rows), range(self.cols))
	
	def __str__(self):
		def zero_bold(i):
			return f'{i}' if i else f'\x1b[1m{i}\x1b[22m'
		return '\n'.join(''.join(zero_bold(value) for value in row) for row in self.map)
	
	def neighbors(self, coords, diagonals=False):
		row, col = coords
		for neighbor_row in [row-1, row, row+1]:
			for neighbor_col in [col-1, col, col+1]:
				if neighbor_col == col and neighbor_row == row:
					continue
				if (0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols
						and (neighbor_row, neighbor_col) != (row, col)):
					if diagonals or neighbor_row == row or neighbor_col == col:
						yield neighbor_row, neighbor_col

@dataclass(slots=True, frozen=True)
class PathStep:
	pathrisk: int
	prev: tuple[int, int] | None

def djikstra(grid: Map, start=(0,0)):
	"""
	Use Djikstra's algorithm to find shortest paths everywhere in the grid
	
	Not a good function: has some infrastructure for more generality than
	needed, but does not actually support that generality.  In another context
	I would rewrite for simplicity.
	
	:param grid: Grid of individual coordinate risks
	:param start: Location to start
	:return: Map of path steps and risks
	"""
	paths = Map([[None for _ in range(grid.cols)] for _ in range(grid.rows)])
	paths[start] = PathStep(0, None)
	to_consider = {neighbor: PathStep(grid[neighbor], start)
	               for neighbor in grid.neighbors(start)}
	while to_consider:
		cur = min(to_consider, key=lambda coord: to_consider[coord].pathrisk)
		step = to_consider[cur]
		assert paths[cur] is None, "Considering path to node when path already found"
		paths[cur] = step
		del to_consider[cur]
		for neighbor in grid.neighbors(cur):
			neighbor_risk = step.pathrisk + grid[neighbor]
			if neighbor not in to_consider and paths[neighbor] is None:
				to_consider[neighbor] = PathStep(neighbor_risk, cur)
			elif neighbor in to_consider:
				assert to_consider[neighbor].pathrisk <= neighbor_risk, "Found better path than candidate"
			else: # paths[neighbor] is not None
				assert paths[neighbor].pathrisk <= neighbor_risk, "Found better path than chosen"
	
	return paths

def iterpath(paths, coords):
	def reverse_iterpath(paths, coords):
		while coords is not None:
			yield coords
			coords = paths[coords].prev
	return reversed(list(reverse_iterpath(paths, coords)))

def main(args):
	map = Map([[int(c) for c in line if c != '\n'] for line in args.input])
	paths = djikstra(map)
	end = map.rows-1, map.cols-1
	info(f'Final path risk: {paths[end].pathrisk}')
	info(f'Final path: {pformat(list(iterpath(paths, end)))}')
	print(f'')

if __name__ == '__main__':
	parser = aoc.get_argparser()
	# Add problem-specifc args here
	args = aoc.parse_args(parser)
	
	main(args)