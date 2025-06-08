#GRAPH SEARCH - SESSION 1

# 1) Representing Search Problems

from abc import ABC, abstractmethod

class Search_problem(ABC):
    @abstractmethod
    def start_node(self):
        pass

    @abstractmethod
    def is_goal(self, node):
        pass

    @abstractmethod
    def neighbors(self, node):
        pass

    def heuristic(self, n):
        return 0

class Edge:
    def __init__(self, from_node, to_node, cost=1, action=None):
        self.from_node = from_node
        self.to_node = to_node
        self.action = action
        self.cost = cost
        assert cost >= 0, (f"Cost cannot be negative: {self}, cost={cost}")
        
    def __repr__(self):
        return f"Edge({self.from_node} -> {self.to_node}, cost={self.cost}, action={self.action})"

# 2)  Explicit Representation of Search Graph

class Search_problem_from_explicit_graph(Search_problem):
    def __init__(self, title, nodes, edges, start, goals, heuristic=None):
        self.title = title
        self.nodes = nodes
        self.edges = edges
        self.start = start
        self.goals = goals
        self.heuristic_dict = heuristic if heuristic else {}

    def start_node(self):
        return self.start

    def is_goal(self, node):
        return node in self.goals

    def neighbors(self, node):
        return [edge for edge in self.edges if edge.from_node == node]

    def heuristic(self, node):
        return self.heuristic_dict.get(node, 0)

    def __repr__(self):
        return f"SearchProblemFromExplicitGraph('{self.title}', {self.nodes}, {self.edges}, start='{self.start}', goals={self.goals}, heuristic={self.heuristic_dict})"

# 3) Paths

class Path:
    def __init__(self, node, edge=None, previous_path=None):
        self.node = node
        self.edge = edge
        self.previous_path = previous_path
        self.total_cost = edge.cost + previous_path.total_cost if edge and previous_path else 0

    def __repr__(self):
        path_str = self.node
        if self.previous_path:
            path_str = f"{self.previous_path} -> {self.node}"
        return f"{path_str} (Total cost: {self.total_cost})"

# 4) Example Search Problems

problem1 = Search_problem_from_explicit_graph('Problem 1',
    {'A', 'B', 'C', 'D', 'G'},
    [Edge('A', 'B', 1), Edge('A', 'C', 1), Edge('B', 'C', 1), Edge('C', 'D', 1),
     Edge('C', 'E', 1)],
    start='B',
    goals={'E'}
)

problem2 = Search_problem_from_explicit_graph('Problem 2',
    {'A','B','C','D','E','G','H','J'},
    [Edge('A','B',1), Edge('B','C',3), Edge('B','D',1), Edge('D','E',3),
    Edge('D','G',1), Edge('A','H',3), Edge('H','J',1)],
    start = 'A',
    goals = {'J'}
)

problem3 = Search_problem_from_explicit_graph('Problem 3',
    {'A', 'B', 'C', 'D', 'E', 'G', 'H', 'J'},
    [Edge('A', 'B', 2), Edge('A', 'C', 3), Edge('A', 'D', 4), Edge('B', 'E', 2), 
     Edge('B', 'F', 3), Edge('C', 'J', 7), Edge('D', 'H', 4), Edge('F', 'D', 2),
     Edge('H', 'G', 3), Edge('J', 'G', 4)],
    start='A',
    goals={'G'}
)

# 5) Searcher

class Searcher:
    def __init__(self, problem):
        self.problem = problem
        self.frontier = [Path(problem.start_node())]

    def search(self):
        while self.frontier:
            path = self.frontier.pop()  
            node = path.node

            if self.problem.is_goal(node):
                return path

            for edge in self.problem.neighbors(node):
                new_path = Path(edge.to_node, edge, path)
                self.frontier.append(new_path)

        return None

# Depth-first search for problem1
print("Paths for problem1 using DFS")
searcher1 = Searcher(problem1)
result = searcher1.search()
while result is not None:
    print(result)
    result = searcher1.search()

# Depth-first search for problem2
print("\nPaths for problem2 using DFS")
searcher2 = Searcher(problem2)
result = searcher2.search()
while result is not None:
    print(result)
    result = searcher2.search()

# Depth-first search for problem3
print("\nPaths for problem3 using DFS")
searcher3 = Searcher(problem3)
result = searcher3.search()
while result is not None:
    print(result)
    result = searcher3.search()
