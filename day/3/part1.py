#!/bin/python

import fileinput

def bits_to_int(bits):
	return int("".join(str(bit) for bit in bits), 2)

counts = None
total = 0

for line in fileinput.input():
	total += 1
	bits = [int(bit) for bit in line.strip()]
	if counts is None:
		counts = [0] * len(bits)
	else:
		assert len(bits) == len(counts)
	
	for i in range(len(counts)):
		counts[i] += bits[i]

cutoff = total / 2
assert not any(count == cutoff for count in counts)
gamma = [int(count > cutoff) for count in counts]
epsilon = [int(not g) for g in gamma]

print(bits_to_int(gamma) * bits_to_int(epsilon))

