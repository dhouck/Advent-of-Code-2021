#!/usr/bin/env python
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

def main(args):
	map = Map([[int(c) for c in line if c != '\n'] for line in args.input])
	total_risk = 0
	for row in range(map.rows):
		for col in range(map.cols):
			height = map.height(row, col)
			if all(height < map.height(*neighbor) for neighbor in map.neighbors(row, col)):
				risk_level = height + 1
				debug(f'Position {row, col} is a valley with risk {risk_level}')
				total_risk += risk_level
			
	info(f'Total risk: {total_risk}')

if __name__ == '__main__':
	parser = aoc.get_argparser()
	# Add problem-specifc args here
	args = aoc.parse_args(parser)
	
	main(args)