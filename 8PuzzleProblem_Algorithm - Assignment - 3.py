import heapq
from collections import deque

#This problem is formulated as a state space search problem
class PuzzleState:
    #Representation for the states and nodes
    def __init__(self, board, parent=None, action=None, cost=0):
        # Parameters:
        # board: The current configuration of the puzzle.
        # parent: The parent state from which this state was generated.
        # action: The move that led to this state.
        # cost: The cost to reach this state from the start state.
        
        self.board = board
        self.parent = parent
        self.action = action
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def is_goal(self, goal):
        return self.board == goal

    def get_blank_position(self):
        return self.board.index(0)

    def generate_children(self):
        # Generate all possible child states from the current state by sliding a tile into the blank space.
        # Returns: A list of child PuzzleState objects.
        
        children = []
        blank_pos = self.get_blank_position()
        moves = [(1, 0, "Down"), (-1, 0, "Up"), (0, 1, "Right"), (0, -1, "Left")]
        x, y = divmod(blank_pos, 3)

        for dx, dy, action in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_blank_pos = nx * 3 + ny
                new_board = self.board[:]
                new_board[blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[blank_pos]
                children.append(PuzzleState(new_board, self, action))

        return children

    def print_solution(self):
        # Recursively print the sequence of moves from the initial state to the goal state.
        if self.parent:
            self.parent.print_solution()
        self.print_board()

    def print_board(self):
        # Print the current board configuration in a 3x3 grid format.
        for i in range(3):
            print(self.board[i*3:(i+1)*3])
        print("\n")

    def get_move_count(self):
        # Count the number of moves from the initial state to the current state.
        if self.parent is None:
            return 0
        return 1 + self.parent.get_move_count()
    
# Breadth-First Search (BFS) - Uninformed Search Strategy
def bfs(start, goal):
    frontier = deque([start])
    explored = set()

    while frontier:
        current = frontier.popleft()

        if current.is_goal(goal):
            current.print_solution()
            move_count = current.get_move_count()
            print(f"Number of moves: {move_count}")
            return move_count

        explored.add(tuple(current.board))

        for child in current.generate_children():
            if tuple(child.board) not in explored:
                frontier.append(child)

# Manhattan Distance as a heuristic
def manhattan_distance(state, goal):
    distance = 0
    for i in range(1, 9):
        current_pos = state.board.index(i)
        goal_pos = goal.index(i)
        current_x, current_y = divmod(current_pos, 3)
        goal_x, goal_y = divmod(goal_pos, 3)
        distance += abs(current_x - goal_x) + abs(current_y - goal_y)
    return distance

# Out-of-sequence as a heuristic
def out_of_sequence(state, goal):
    score = 0
    for i in range(8):
        if i == 4:  
            if state.board[i] != goal[i]:
                score += 1
        elif state.board[i] != 0 and state.board[i] != goal[i]:
            score += 2
    return score

# Greedy Best-First Search
def greedy_best_first_search(start, goal, heuristic):
    frontier = []
    heapq.heappush(frontier, (heuristic(start, goal), start))
    explored = set()

    while frontier:
        _, current = heapq.heappop(frontier)

        if current.is_goal(goal):
            current.print_solution()
            move_count = current.get_move_count()
            print(f"Number of moves: {move_count}")
            return move_count

        explored.add(tuple(current.board))

        for child in current.generate_children():
            if tuple(child.board) not in explored:
                heapq.heappush(frontier, (heuristic(child, goal), child))

# A* Search 
def a_star_search(start, goal, heuristic):
    frontier = []
    heapq.heappush(frontier, (heuristic(start, goal), start))
    explored = set()

    while frontier:
        _, current = heapq.heappop(frontier)

        if current.is_goal(goal):
            current.print_solution()
            move_count = current.get_move_count()
            print(f"Number of moves: {move_count}")
            return move_count

        explored.add(tuple(current.board))

        for child in current.generate_children():
            new_cost = current.cost + 1
            if tuple(child.board) not in explored or new_cost < child.cost:
                child.cost = new_cost
                priority = new_cost + heuristic(child, goal)
                heapq.heappush(frontier, (priority, child))

# Puzzle State Example
start_state = PuzzleState([1, 2, 3, 4, 0, 5, 6, 7, 8])
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Store the number of moves for each search method and heuristic
results = {}

# Breadth-First Search (BFS)
print("Breadth-First Search:")
results['BFS'] = bfs(start_state, goal_state)

# Greedy Best-First Search with Manhattan Distance
print("\nGreedy Best-First Search with Manhattan Distance:")
results['Greedy Best-First (Manhattan Distance)'] = greedy_best_first_search(start_state, goal_state, manhattan_distance)

# A* Search with Manhattan Distance
print("\nA* Search with Manhattan Distance:")
results['A* (Manhattan Distance)'] = a_star_search(start_state, goal_state, manhattan_distance)

# Greedy Best-First Search with Out-of-sequence Score
print("\nGreedy Best-First Search with Out-of-sequence Score:")
results['Greedy Best-First (Out-of-sequence Score)'] = greedy_best_first_search(start_state, goal_state, out_of_sequence)

# A* Search with Out-of-sequence Score
print("\nA* Search with Out-of-sequence Score:")
results['A* (Out-of-sequence Score)'] = a_star_search(start_state, goal_state, out_of_sequence)

# Summary of the number of moves for each strategy
print("\nSummary of Number of Moves:")
for method, moves in results.items():
    print(f"{method}: {moves} moves")
