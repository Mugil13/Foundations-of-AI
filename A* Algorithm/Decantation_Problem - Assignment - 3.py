from collections import deque

# Define the state of the water jugs
class WaterJugState:
    def __init__(self, jugs, parent=None, action=None):
        self.jugs = jugs
        self.parent = parent
        self.action = action

    def is_goal(self, goal_state):
        return self.jugs == goal_state

    def __eq__(self, other):
        return self.jugs == other.jugs

    def __hash__(self):
        return hash(self.jugs)

# Generate all possible next states from the current state
def next_states(state):
    successors = []
    jug_sizes = (8, 5, 3)  

    for i in range(3):
        for j in range(3):
            if i != j:
                new_jugs = list(state.jugs)
                transfer_amount = min(new_jugs[i], jug_sizes[j] - new_jugs[j])
                new_jugs[i] -= transfer_amount
                new_jugs[j] += transfer_amount

                action = f"Pour {transfer_amount}L from jug {i+1} to jug {j+1}"
                successors.append(WaterJugState(tuple(new_jugs), state, action))

    return successors

# Perform BFS to find a solution state that matches the goal state
def bfs(initial_state, goal_state):
    #Queue as a frontier
    frontier = deque([initial_state])
    explored = {}
    state_count = 0

    while frontier:
        current_state = frontier.popleft()
        state_count += 1
        if current_state.is_goal(goal_state):
            return current_state, state_count
        explored[current_state.jugs] = current_state

        for next_state in next_states(current_state):
            if next_state.jugs not in explored and all(next_state.jugs != s.jugs for s in frontier):
                frontier.append(next_state)

    return None, state_count

# Print the sequence of states and actions from initial to goal state
def print_solution(state):
    if state.parent:
        print_solution(state.parent)
    # Print the current state and action leading to this state
    action_str = state.action if state.action else "None"
    print(f"State: {state.jugs}, Action: {action_str}")

# Get the target state from the user
goal_state = tuple(map(int, input("Enter the goal state as three integers (e.g., 4 1 3): ").split()))

# Initial state of the water jugs
initial_state = WaterJugState((8, 0, 0))

goal_state, explored_states = bfs(initial_state, goal_state)

if goal_state:
    print("Solution found:")
    print_solution(goal_state)
    print(f"Goal state reached: {goal_state.jugs}")
    print(f"Total states explored: {explored_states}")
else:
    print("No solution found")
