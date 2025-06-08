#UNIFORM COST SEARCH AND DIJKSTRA ALGORITHM - SESSION 2

# 1) Representing search problems

from abc import ABC, abstractmethod
import heapq

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
    
# 2) Explicit Representation of Search Graph

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
        if self.previous_path is None:
            return f"{self.node}"
        else:
            return f"{self.previous_path} -> {self.node}"

    def get_full_path(self):
        if self.previous_path is None:
            return self.node
        else:
            return self.previous_path.get_full_path() + " -> " + self.node

    def get_total_cost(self):
        return self.total_cost
    
# 4) Example Search Problems

problem1 = Search_problem_from_explicit_graph('Problem 1',
    {'A', 'B', 'C', 'D', 'G'},
    [Edge('A', 'B', 3), Edge('A', 'C', 1), Edge('B', 'D', 1), Edge('B', 'G', 3),
     Edge('C', 'B', 1), Edge('C', 'D', 3), Edge('D', 'G', 1)],
    start='A',
    goals={'D'}
)

problem2 = Search_problem_from_explicit_graph('Problem 2',
    {'A','B','C','D','E','G','H','J'},
    [Edge('A','B',1), Edge('B','C',3), Edge('B','D',1), Edge('D','E',3),
    Edge('D','G',1), Edge('A','H',3), Edge('H','J',1)],
    start = 'A',
    goals = {'H'}
)

problem3 = Search_problem_from_explicit_graph('Problem 3',
    {'A', 'B', 'C', 'D', 'E', 'G', 'H', 'J'},
    [Edge('A', 'B', 2), Edge('A', 'C', 3), Edge('A', 'D', 4), Edge('B', 'E', 2), 
     Edge('B', 'F', 3), Edge('C', 'J', 7), Edge('D', 'H', 4), Edge('F', 'D', 2),
     Edge('H', 'G', 3), Edge('J', 'G', 4)],
    start='A',
    goals={'J'}
)

# 5) Frontier as a Priority Queue

class FrontierPQ:
    def __init__(self):
        self.elements = []
        self.counter = 0  

    def add(self, path):
        heapq.heappush(self.elements, (path.total_cost, self.counter, path))
        self.counter += 1

    def pop(self):
        return heapq.heappop(self.elements)[2]

    def is_empty(self):
        return len(self.elements) == 0

# 6) Searcher

class Searcher:
    def __init__(self, problem):
        self.problem = problem
        self.frontier = FrontierPQ()
        self.frontier.add(Path(problem.start_node()))
        self.explored = set()

    def search(self):
        while not self.frontier.is_empty():
            path = self.frontier.pop()
            node = path.node

            if self.problem.is_goal(node):
                return path

            if node not in self.explored:
                self.explored.add(node)
                for edge in self.problem.neighbors(node):
                    new_path = Path(edge.to_node, edge, path)
                    self.frontier.add(new_path)

        return None

#Dijkstra search for problem1
print("Paths for problem 1 using Dijkstra's algorithm")
searcher1 = Searcher(problem1)
result = searcher1.search()
if result:
    print("Path:", result.get_full_path())
    print("Total Cost:", result.get_total_cost())

# Dijkstra search for problem2
print("\nPaths for problem 2 using Dijkstra's algorithm")
searcher2 = Searcher(problem2)
result = searcher2.search()
if result:
    print("Path:", result.get_full_path())
    print("Total Cost:", result.get_total_cost())

# Dijkstra search for problem3
print("\nPaths for problem 3 using Dijkstra's algorithm")
searcher3 = Searcher(problem3)
result = searcher3.search()
if result:
    print("Path:", result.get_full_path())
    print("Total Cost:", result.get_total_cost())
