# Session 5: DFS Solver for CSP — N-Queens Problem

# 1) Class Variable
class Variable:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain

    def __repr__(self):
        return f"Variable({self.name}, {self.domain})"

# 2) Class Constraint
class Constraint:
    def __init__(self, scope, condition, name=None):
        self.scope = scope  # List of variables
        self.condition = condition  # Condition function
        self.name = name if name else condition.__name__  # Default name is the function's name

    def can_evaluate(self, assignment):
        return all(var in assignment for var in self.scope)

    def holds(self, assignment):
        if not self.can_evaluate(assignment):
            return False
        values = [assignment[var] for var in self.scope]
        return self.condition(*values)

# 3) Class CSP
class CSP:
    def __init__(self, name, variables, constraints):
        self.name = name
        self.variables = variables
        self.constraints = constraints
        self.var_to_const = {var: set() for var in variables}
        
        for constraint in constraints:
            for var in constraint.scope:
                self.var_to_const[var].add(constraint)

    def consistent(self, assignment):
        # Returns True if the assignment is consistent with all constraints.
        for constraint in self.constraints:
            if constraint.can_evaluate(assignment) and not constraint.holds(assignment):
                return False
        return True
    
# 4) 8 - Queens
# Not attacking condition
def not_attacking(row1, col1, row2, col2):
    return row1 != row2 and abs(row1 - row2) != abs(col1 - col2)

def different_rows(*args):
    return len(set(args)) == len(args)

# Defining the constraints
columns = range(8)
variables = [Variable(f'Q{col}', list(range(8))) for col in columns]

constraints = []
constraints.append(Constraint(variables, different_rows))

# Add constraints for diagonal attacks
for col1 in columns:
    for col2 in range(col1 + 1, 8):
        constraints.append(
            Constraint(
                [variables[col1], variables[col2]],
                lambda row1, row2, col1=col1, col2=col2: not_attacking(row1, col1, row2, col2)
            )
        )

# Create CSP for 8-Queens
csp_8_queens = CSP("8-Queens", variables, constraints)

# 5) Simple DFS Solver
# DFS Solution
def dfs_solver(csp, variable_order=None):
    if variable_order is None:
        variable_order = list(csp.variables)

    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            yield assignment
            return

        var = next(v for v in variable_order if v not in assignment)
        for value in var.domain:
            local_assignment = assignment.copy()
            local_assignment[var] = value

            if csp.consistent(local_assignment):
                yield from backtrack(local_assignment)

    return backtrack({})

# Printing the solution
def print_8_queens_solution(solution):
    board = [['.'] * 8 for _ in range(8)]  
    for var, row in solution.items():
        col = int(var.name[1])  
        board[row][col] = 'Q'
    
    for row in board:
        print(" ".join(row))
    print("\n")

solutions = dfs_solver(csp_8_queens)

for idx, solution in enumerate(solutions, 1):
    word = str(input(("Enter Yes to see the next solution, else Enter No to exit the program: ")))
    if word == "Yes":
        print(f"Solution {idx}:")
        print_8_queens_solution(solution)
    elif word == "No":
        print("Exiting")
        break
    else:
        print("Invalid Command")

