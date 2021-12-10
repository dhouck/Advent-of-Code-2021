#!/usr/bin/env python
from dataclasses import dataclass
from logging import debug, info, warning, error, exception, critical
from pprint import pprint, pformat

import aoc

@dataclass(slots=True, frozen=True)
class Bracket:
	open: str
	close: str
	corrupted_value: int
	completion_value: int

BRACKETS = {
	Bracket('(', ')', 3, 1),
	Bracket('[', ']', 57, 2),
	Bracket('{', '}', 1197, 3),
	Bracket('<', '>', 25137, 4),
}

OPENING = {bracket.open: bracket for bracket in BRACKETS}
CLOSING = {bracket.close: bracket for bracket in BRACKETS}

def main(args):
	corrupted_score = 0
	completion_scores = []
	for line in args.input:
		stack = []
		for c in line.strip():
			if c in '([{<':
				stack.append(c)
			else:
				opening = stack.pop()
				bracket = CLOSING[c]
				if bracket.open != opening:
					corrupted_score += bracket.corrupted_value
					break  # Line corrupt; go to next
		else:  # Didn't break out of loop
			if stack:
				finish = [OPENING[c] for c in reversed(stack)]
				score = 0
				for bracket in finish:
					score *= 5
					score += bracket.completion_value
				debug(f'Incomplete line; to finish add {"".join(bracket.close for bracket in finish)} (score {score})')
				completion_scores.append(score)
			else:
				info(f'Complete line: {line.strip()}')
	
	print(f'Corruption score: {corrupted_score}')
	info(f'There are {len(completion_scores)} completed lines.')
	debug(pformat(sorted(completion_scores)))
	print(f'Completion score: {sorted(completion_scores)[(len(completion_scores)) // 2]}')

if __name__ == '__main__':
	parser = aoc.get_argparser()
	# Add problem-specifc args here
	args = aoc.parse_args(parser)
	
	main(args)