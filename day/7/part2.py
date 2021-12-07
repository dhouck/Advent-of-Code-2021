import fileinput

from collections import Counter

def parse_input(line):
	c = Counter(int(fish) for fish in line.split(','))
	return sorted(c.elements())

crabs = parse_input(fileinput.input().readline())
cheapest = 488 # (sum(crabs) + (len(crabs) // 2)) // len(crabs)
print(f"Cheapest position is {cheapest}")
print(f'Non-integer optimum is {sum(crabs) / len(crabs)} ({sum(crabs)}/{len(crabs)})')
absolute_deltas = [abs(pos - cheapest) for pos in crabs]
print(f"Fuel cost: {sum(Δ*(Δ+1)//2 for Δ in absolute_deltas)}")
