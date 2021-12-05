import collections
import fileinput
import itertools

from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Point:
	x: int
	y: int
	
	@staticmethod
	def parse(s: str) -> 'Point':
		x, y = (int(coord) for coord in s.split(','))
		return Point(x, y)

def inclusive_updown_range(begin, end):
	if begin < end:
		return range(begin, end+1)
	elif begin > end:
		return range(begin, end-1, -1)
	else:
		return itertools.repeat(begin)

def mark_line(map, begin: Point, end: Point):
	if begin == end:
		map[begin] += 1
		return
	
	x_range = inclusive_updown_range(begin.x, end.x)
	y_range = inclusive_updown_range(begin.y, end.y)
	for x, y in zip(x_range, y_range):
		map[Point(x, y)] += 1

points = collections.Counter()
for line in fileinput.input():
	begin, end = line.strip().split(' -> ')
	mark_line(points, Point.parse(begin), Point.parse(end))

multiline_points = [point for point, count in points.items() if count > 1]
print(f"There are {len(multiline_points)} points with more than 1 line")