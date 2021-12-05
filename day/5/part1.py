import collections
import fileinput

from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Point:
	x: int
	y: int
	
	@staticmethod
	def parse(s: str) -> 'Point':
		x, y = (int(coord) for coord in s.split(','))
		return Point(x, y)

def mark_line(map, begin: Point, end: Point):
	if begin.x != end.x and begin.y != end.y:
		return  # Only consider horizontal/vertical for now
	elif begin == end:
		map[begin] += 1
	elif begin.x == end.x:
		x = begin.x
		first, second = sorted([begin.y, end.y])
		for y in range(first, second + 1):
			map[Point(x, y)] += 1
	else:
		assert begin.y == end.y and begin.x != end.x
		y = begin.y
		first, second = sorted([begin.x, end.x])
		for x in range(first, second + 1):
			map[Point(x, y)] += 1

points = collections.Counter()
for line in fileinput.input():
	begin, end = line.strip().split(' -> ')
	mark_line(points, Point.parse(begin), Point.parse(end))

print(f"There are {len([point for point, count in points.items() if count > 1])} points with more than 1 line")