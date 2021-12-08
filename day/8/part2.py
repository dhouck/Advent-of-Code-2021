#!/usr/bin/env python

import fileinput

DIGITS = {
	'abcefg': 0,
	'cf': 1,
	'acdeg': 2,
	'acdfg': 3,
	'bcdf': 4,
	'abdfg': 5,
	'abdefg': 6,
	'acf': 7,
	'abcdefg': 8,
	'abcdfg': 9,
}

def parse_line(line):
	samples, data = line.split('|')
	return [set(sample) for sample in samples.split()], data.split()

def analyze(samples):
	cf = [sample for sample in samples if len(sample) == 2][0]
	# print(f"CF: {cf}")
	a = ([sample for sample in samples if len(sample) == 3][0] - cf).pop()
	# print(f"A: {a}")
	bd = [sample for sample in samples if len(sample) == 4][0] - cf
	# print(f"BD: {bd}")
	
	five_segments = [sample for sample in samples if len(sample) == 5]
	acdfg = [sample for sample in five_segments if sample > cf][0]
	# print(f"ACDFG: {acdfg}")
	dg = acdfg - cf - {a}
	# print(f'DG: {dg}')
	b = (bd - dg).pop()
	d = (dg & bd).pop()
	g = (dg - bd).pop()
	e = (set('abcdefg') - acdfg - {b}).pop()
	
	acdeg = [sample for sample in five_segments if e in sample][0]
	c = (acdeg - {a, d, e, g}).pop()
	f = (cf - {c}).pop()
	
	return {a: 'a', b: 'b', c: 'c', d: 'd', e: 'e', f: 'f', g: 'g'}

def decode(mapping, data):
	def decode_digit(mapping, digit):
		return DIGITS[''.join(sorted(mapping[segment] for segment in digit))]
	
	result = 0
	for digit in data:
		result *= 10
		result += decode_digit(mapping, digit)
	return result

total = 0
for line in fileinput.input():
	samples, data = parse_line(line)
	mapping = analyze(samples)
	total += decode(mapping, data)

print(total)