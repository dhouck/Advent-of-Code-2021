#!/usr/bin/python

import cmd
import dataclasses

@dataclasses.dataclass(slots=True)
class Coordinates:
	depth: int = 0
	horizontal: int = 0
	aim: int = 0

class SubMoveCommand(cmd.Cmd):
	__slots__ = ("coords",)
	intro = "Please enter the submarine path:\n"
	prompt = "(submarine) "
	
	def __init__(self, coords: Coordinates = None):
		super().__init__()
		if coords is not None:
			self.coords = coords
		else:
			self.coords = Coordinates()
	
	def do_forward(self, args):
		self.coords.horizontal += int(args)
		self.coords.depth += int(args) * self.coords.aim
	def do_up(self, args):
		self.coords.aim -= int(args)
	def do_down(self, args):
		self.coords.aim += int(args)
	def do_EOF(self, args):
		return True

def main():
	coords = Coordinates()
	SubMoveCommand(coords).cmdloop()
	print(coords)
	print(coords.depth * coords.horizontal)

if __name__ == "__main__":
	main()