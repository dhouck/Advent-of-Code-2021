#!/usr/bin/env python
from dataclasses import dataclass
from logging import debug, info, warning, error, exception, critical
from pprint import pprint, pformat
import aoc

@dataclass(slots=True, frozen=True, order=True)
class Point:
	x: int
	y: int

def plot(points):
	max_x = max(p.x for p in points) + 1
	max_y = max(p.y for p in points) + 1
	return '\n'.join(''.join('█' if Point(x,y) in points else ' '
	                         for x in range(max_x))
	                 for y in range(max_y))

def main(args):
	points = set()
	lines = list(line.strip() for line in args.input)
	num = [i for i, line in enumerate(lines) if not line][0]
	for line in lines[:num]:
		point = Point(*(int(coord) for coord in line.split(',')))
		debug(f'Adding point: {point}')
		points.add(point)
	info(f'There were {len(points)} distinct points')
	
	for i, line in enumerate(lines[num+1:]):
		axis, position = line.split()[-1].split('=')
		position = int(position)
		info(f'Folding along {axis}={position}')
		if axis == 'x':
			for p in {point for point in points if point.x > position}:
				debug(f'Folding point {p}')
				points.add(Point(position * 2 - p.x, p.y))
				points.remove(p)
				assert position * 2 - p.x >= 0
		else:
			for p in {point for point in points if point.y > position}:
				debug(f'Folding point {p}')
				points.add(Point(p.x, position * 2 - p.y))
				points.remove(p)
				assert position * 2 - p.y >= 0
		print(f"After fold {i+1}, there are {len(points)} points left")
		debug(f'Points: {pformat(sorted(points))}')
	
	print(plot(points))

if __name__ == '__main__':
	parser = aoc.get_argparser()
	# Add problem-specifc args here
	args = aoc.parse_args(parser)
	
	main(args)