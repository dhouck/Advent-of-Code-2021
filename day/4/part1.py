import fileinput

class Board:
	__slots__ = "board"
	
	COLS = 5
	ROWS = 5
	
	def __init__(self, lines):
		self.board = [[int(cell) for cell in line.split()] for line in lines]
		assert len(self.board) == self.ROWS
		assert all(len(row) == self.COLS for row in self.board)
	
	def mark(self, num) -> int:
		marked = 0
		for row in self.board:
			for col_idx, cell in enumerate(row):
				if cell == num:
					marked += 1
					row[col_idx] = None
		assert marked <= 1, f"Marked too many cells: {marked}"
		return marked
	
	def check(self) -> bool:
		def check_line(line):
			return all(cell is None for cell in line)
		
		for row in self.board:
			if check_line(row): return True
		
		for col_idx in range(self.COLS):
			col = [row[col_idx] for row in self.board]
			if check_line(col): return True
		
		return False
	
	def partial_score(self) -> int:
		return sum(cell for row in self.board for cell in row if cell is not None)

def parse(lines):
	calls = [int(call) for call in lines[0].split(',')]
	
	assert not lines[1], "Line 2 of input must be blank"
	prev_blank = 1
	boards = []
	for line_no in range(2, len(lines)):
		if not lines[line_no]:
			boards.append(Board(lines[prev_blank+1 : line_no]))
			prev_blank = line_no
	boards.append(Board(lines[prev_blank+1 :]))
	return calls, boards

def main():
	calls, boards = parse([line.strip() for line in fileinput.input()])
	
	bingos = set()
	print(f'Playing bingo on {len(boards)} boards')
	for call in calls:
		print(f"Call: {call}")
		cur_bingo = 0
		for num, board in enumerate(boards):
			if num in bingos: continue
			if board.mark(call):
				if board.check():
					print(f"BINGO: Board #{num} scores {call * board.partial_score()}")
					bingos.add(num)
					cur_bingo += 1
		match cur_bingo:
			case 0:
				pass
			case 1:
				print()
			case _:
				print(f"{cur_bingo} bingos this call")
				print()
		
		if len(bingos) == len(boards):
			print("All boards have reached bingo.")
			break5

if __name__ == "__main__":
	main()