from random import randint

# Set the board size (8x8)
N = 8

# Randomly configure the board with queens at random positions
def configureRandomly(board, state):
	for i in range(N):
		state[i] = randint(0, 100000) % N
		board[state[i]][i] = 1

def printBoard(board):
	for i in range(N):
		print(' '.join("Q" if board[i][j] == 1 else "." for j in range(N)))

# Print the state (positions of queens on the board)
def printState(state):
	print(*state)

# Compare two states to see if they are the same
def compareStates(state1, state2):
	for i in range(N):
		if state1[i] != state2[i]:
			return False
	return True

# Fill the board with a given value (used to reset the board)
def fill(board, value):
	for i in range(N):
		for j in range(N):
			board[i][j] = value

# Calculate the number of attacking queens on the board
def calculateObjective(board, state):
	attacking = 0
	for i in range(N):
		row = state[i]
		
		# Check left in the row
		col = i - 1
		while col >= 0 and board[row][col] != 1:
			col -= 1
		if col >= 0 and board[row][col] == 1:
			attacking += 1

		# Check right in the row
		col = i + 1
		while col < N and board[row][col] != 1:
			col += 1
		if col < N and board[row][col] == 1:
			attacking += 1

		# Check upper-left diagonal
		row = state[i] - 1
		col = i - 1
		while col >= 0 and row >= 0 and board[row][col] != 1:
			col -= 1
			row -= 1
		if col >= 0 and row >= 0 and board[row][col] == 1:
			attacking += 1

		# Check lower-right diagonal
		row = state[i] + 1
		col = i + 1
		while col < N and row < N and board[row][col] != 1:
			col += 1
			row += 1
		if col < N and row < N and board[row][col] == 1:
			attacking += 1

		# Check lower-left diagonal
		row = state[i] + 1
		col = i - 1
		while col >= 0 and row < N and board[row][col] != 1:
			col -= 1
			row += 1
		if col >= 0 and row < N and board[row][col] == 1:
			attacking += 1

		# Check upper-right diagonal
		row = state[i] - 1
		col = i + 1
		while col < N and row >= 0 and board[row][col] != 1:
			col += 1
			row -= 1
		if col < N and row >= 0 and board[row][col] == 1:
			attacking += 1

	return int(attacking / 2)  

# Board Creation
def generateBoard(board, state):
	fill(board, 0)
	for i in range(N):
		board[state[i]][i] = 1  

def copyState(state1, state2):
	for i in range(N):
		state1[i] = state2[i]

# Get the neighbor of the current state (modifying one queen's position)
def getNeighbour(board, state):
	opBoard = [[0 for _ in range(N)] for _ in range(N)]
	opState = [0 for _ in range(N)]

	copyState(opState, state)
	generateBoard(opBoard, opState)

	opObjective = calculateObjective(opBoard, opState)

	NeighbourBoard = [[0 for _ in range(N)] for _ in range(N)]
	NeighbourState = [0 for _ in range(N)]
	copyState(NeighbourState, state)
	generateBoard(NeighbourBoard, NeighbourState)

	for i in range(N):
		for j in range(N):
			if j != state[i]:
				NeighbourState[i] = j
				NeighbourBoard[NeighbourState[i]][i] = 1
				NeighbourBoard[state[i]][i] = 0
				temp = calculateObjective(NeighbourBoard, NeighbourState)

				# If the new state is better or equal, update the state
				if temp <= opObjective:
					opObjective = temp
					copyState(opState, NeighbourState)
					generateBoard(opBoard, opState)

				# Undo the move and restore the original state
				NeighbourBoard[NeighbourState[i]][i] = 0
				NeighbourState[i] = state[i]
				NeighbourBoard[state[i]][i] = 1

	# Update the current state to the best neighbor found
	copyState(state, opState)
	fill(board, 0)
	generateBoard(board, state)

# Hill climbing algorithm to solve the N-Queens problem
def hillClimbing(board, state):

	neighbourBoard = [[0 for _ in range(N)] for _ in range(N)]
	neighbourState = [0 for _ in range(N)]

	copyState(neighbourState, state)
	generateBoard(neighbourBoard, neighbourState)

	while True:
		copyState(state, neighbourState)
		generateBoard(board, state)
		getNeighbour(neighbourBoard, neighbourState)

		# If the state does not change, print the solution
		if compareStates(state, neighbourState):
			printBoard(board)
			break
		
		# If the objective value remains the same, randomize a queen's position
		elif calculateObjective(board, state) == calculateObjective(neighbourBoard, neighbourState):
			neighbourState[randint(0, 100000) % N] = randint(0, 100000) % N
			generateBoard(neighbourBoard, neighbourState)

# Function calls
state = [0] * N
board = [[0 for _ in range(N)] for _ in range(N)]
configureRandomly(board, state)

hillClimbing(board, state)
