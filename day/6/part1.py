#!/usr/bin/env python
import argparse
import sys

from collections import Counter
from pprint import pprint

def advance(fish_counts):
	spawning = fish_counts[0]
	new_counts = fish_counts[1:]
	new_counts[6] += spawning
	new_counts.append(spawning)
	return new_counts

def parse_input(line):
	c = Counter(int(fish) for fish in line.split(','))
	assert set(range(9)).issuperset(set(c.keys()))
	return [c[i] for i in range(9)]

def main():
	parser = argparse.ArgumentParser(description='Calculate fish population')
	parser.add_argument('-d', '--days', type=int, default=18,
	                    help='How many days in advance to calculate fish population')
	parser.add_argument('input', type=argparse.FileType('r'), default=sys.stdin)
	args = parser.parse_args()
	fish = parse_input(args.input.readline())
	for i in range(args.days):
		# pprint(fish)
		fish = advance(fish)
	
	pprint(fish)
	print(f'Total: {sum(fish)}')

if __name__ == '__main__':
	main()