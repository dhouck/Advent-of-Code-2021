#!/usr/bin/env python
import coloredlogs
import itertools
from logging import debug, info, warning, error, exception, critical
from pprint import pprint, pformat

import aoc

# Modified from day 9
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
	
	def neighbors(self, row, col):
		# Exceptions are cheap in Python
		for neighbor_row in [row-1, row, row+1]:
			for neighbor_col in [col-1, col, col+1]:
				if neighbor_col == col and neighbor_row == row:
					continue
				if (0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols
				    and (neighbor_row, neighbor_col) != (row, col)):
					yield neighbor_row, neighbor_col
	
	def advance(self) -> int:
		debug('Advancing…')
		debug(f'Initial map:\n{self}')
		# Step 1: increase energy
		for coords in self:
			self[coords] += 1
		
		# Step 2: Flash
		flash = [[False for _ in range(self.cols)] for _ in range(self.rows)]
		another_pass = True
		total = 0
		while another_pass:
			another_pass = False
			for row, col in self:
				if self[row, col] > 9 and not flash[row][col]:
					debug(f"Flashing {row, col}")
					flash[row][col] = True
					total += 1
					another_pass = True
					for neighbor in self.neighbors(row, col):
						self[neighbor] += 1
		
		# Step 3: Reset
		if total:
			for coords in self:
				if self[coords] > 9:
					self[coords] = 0
		
		return total

def main(args):
	map = Map([[int(c) for c in line if c != '\n'] for line in args.input])
	info(f'Advancing for {args.rounds} rounds.')
	synchronized = False
	total = 0
	for round in range(args.rounds):
		debug(f'Round {round + 1}')
		flashes = map.advance()
		if flashes == map.rows * map.cols:
			if not synchronized:
				print(f'First synchronization at {round+1}')
			synchronized = True
	print(f"Total flashes: {sum(map.advance() for _ in range(args.rounds))}")

if __name__ == '__main__':
	parser = aoc.get_argparser()
	parser.add_argument('-r', '--rounds', type=int, default=100)
	# Add problem-specifc args here
	args = aoc.parse_args(parser)
	
	main(args)