#!/usr/bin/env python
from dataclasses import dataclass
from logging import debug, info, warning, error, exception, critical
from pprint import pprint, pformat

import aoc

@dataclass(slots=True, frozen=True)
class Bracket:
	open: str
	close: str
	value: int

BRACKETS = {
	Bracket('(', ')', 3),
	Bracket('[', ']', 57),
	Bracket('{', '}', 1197),
	Bracket('<', '>', 25137),
}

OPENING = {bracket.open: bracket for bracket in BRACKETS}
CLOSING = {bracket.close: bracket for bracket in BRACKETS}

def main(args):
	score = 0
	for line in args.input:
		stack = []
		for c in line.strip():
			if c in '([{<':
				stack.append(c)
			else:
				opening = stack.pop()
				bracket = CLOSING[c]
				if bracket.open != opening:
					score += bracket.value
					continue  # Line corrupt; go to next
		if stack:
			finish = [OPENING[c].close for c in reversed(stack)]
			info(f'Incomplete line; to finish add {"".join(finish)}')
		
	print(f'Total score: {score}')

if __name__ == '__main__':
	parser = aoc.get_argparser()
	# Add problem-specifc args here
	args = aoc.parse_args(parser)
	
	main(args)