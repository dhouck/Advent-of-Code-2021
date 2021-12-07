import fileinput

from collections import Counter

def parse_input(line):
	c = Counter(int(fish) for fish in line.split(','))
	return sorted(c.elements())
	
crabs = parse_input(fileinput.input().readline())
cheapest = crabs[len(crabs)//2]
print(f"Cheapest position is {cheapest}")
if len(crabs) % 2 == 0:
	alternate = crabs[len(crabs)//2 - 1]
	if alternate != cheapest:
		print(f"(Tied with {alternate})")
print(f"Fuel cost: {sum(abs(pos - cheapest) for pos in crabs)}")
