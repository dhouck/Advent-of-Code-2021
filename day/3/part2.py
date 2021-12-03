#!/usr/bin/env python

import fileinput

def bits_to_int(bits):
	return int("".join(str(bit) for bit in bits), 2)

def bit_counts(bits_list):
	counts = None
	for bits in bits_list:
		if counts is None:
			counts = [0] * len(bits)
		else:
			assert len(bits) == len(counts)
		
		for i in range(len(counts)):
			counts[i] += bits[i]
	return counts

def read_report():
	return [[int(bit) for bit in line.strip()] for line in fileinput.input()]

def recursive_filter(report, func, pos=0):
	counts = bit_counts(report)
	desired_bit = func(counts[pos], len(report))
	filtered = [value for value in report if value[pos] == desired_bit]
	match len(filtered):
		case 0:
			# Shouldn't happen
			raise ValueError("Recursive filter removed all values")
		case 1:
			return bits_to_int(filtered[0])
		case _:
			return recursive_filter(filtered, func, pos + 1)


report = read_report()
print("Calculating oxygen…")
oxygen = recursive_filter(report, lambda count, total: count >= total/2)
print()
print("Calculating CO₂…")
co2 = recursive_filter(report, lambda count, total: count < total/2)
print()
print(f"Oxygen value: {oxygen}\nCO₂ value: {co2}\nProduct: {oxygen * co2}")