# Session 6: MiniMax Algorithm and Alpha-Beta Pruning

# Class Node to initialize, add children and evaluate inequality
class Node:
    def __init__(self, name, isMax, value=None, range_value=None):
        self.name = name
        self.isMax = isMax
        self.value = value
        self.range_value = range_value  # Inequality attribute
        self.children = []  # Children Node List

    def add_child(self, child_node):
        self.children.append(child_node)

    def evaluate(self):
        if self.value is not None:
            return self.value
        elif self.range_value is not None:
            if self.range_value.startswith('<='):
                return float(self.range_value[2:])  
            elif self.range_value.startswith('>='):
                return float(self.range_value[2:])  
        return float('-inf')  

# 1) Minimax algorithm for a zero-sum two player game as a function minimax(node, depth).

def minimax(node, depth):
    if not node.children or depth == 0:  
        return node.evaluate(), [node.name]

    if node.isMax:
        max_eval = float('-inf')
        best_path = []
        for child in node.children:
            eval, path = minimax(child, depth - 1)
            if eval > max_eval:
                max_eval = eval
                best_path = path
        return max_eval, [node.name] + best_path
    else:
        min_eval = float('inf')
        best_path = []
        for child in node.children:
            eval, path = minimax(child, depth - 1)
            if eval < min_eval:
                min_eval = eval
                best_path = path
        return min_eval, [node.name] + best_path

# 2) Minimax with alpha-beta pruning including inequality handling

def minimax_alpha_beta(node, depth, alpha=float('-inf'), beta=float('inf')):
    if not node.children or depth == 0:  # Leaf node or depth limit
        return node.evaluate(), [node.name]

    if node.isMax:
        max_eval = float('-inf')
        best_path = []
        for child in node.children:
            eval, path = minimax_alpha_beta(child, depth - 1, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_path = path
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # β cutoff
        return max_eval, [node.name] + best_path
    else:
        min_eval = float('inf')
        best_path = []
        for child in node.children:
            eval, path = minimax_alpha_beta(child, depth - 1, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_path = path
            beta = min(beta, eval)
            if beta <= alpha:
                break  # α cutoff
        return min_eval, [node.name] + best_path

# Game Tree simulation using MiniMax Algorithm and Alpha-Beta Pruning
# Creating the game tree

root = Node("A", isMax=True)
b = Node("B", isMax=False)
c = Node("C", isMax=False)
d = Node("D", isMax=False)
e = Node("E", isMax=True)
f = Node("F", isMax=True)
g = Node("G", isMax=True)
h = Node("H", isMax=True)
i = Node("I", isMax=True)
j = Node("J", isMax=True)
k = Node("K", isMax=True)
l = Node("L", isMax=False)
m = Node("M", isMax=False)
n = Node("N", isMax=False)
o = Node("O", isMax=False)
p = Node("P", isMax=False)
q = Node("Q", isMax=False)
r = Node("R", isMax=False)
s = Node("S", isMax=False)
t = Node("T", isMax=False)
u = Node("U", isMax=False)
v = Node("V", isMax=False)
w = Node("W", isMax=True, value=15)
x = Node("X", isMax=True, value=16)
y = Node("Y", isMax=True, value=14)
z = Node("Z", isMax=True, value=13)
a1 = Node("A1", isMax=True, value=12)
a2 = Node("A2", isMax=True, value=16)
a3 = Node("A3", isMax=True, value=18)
a4 = Node("A4", isMax=True, value=11)
a5 = Node("A5", isMax=True, value=16)
a6 = Node("A6", isMax=True, value=14)
a7 = Node("A7", isMax=True, value=18)
a8 = Node("A8", isMax=True, value=15)
a9 = Node("A9", isMax=True, value=13)
a10 = Node("A10", isMax=True, value=16)
a11 = Node("A11", isMax=True, value=16)
a12 = Node("A12", isMax=True, value=14)
a13 = Node("A13", isMax=True, value=13)
a14 = Node("A14", isMax=True, value=10)
a15 = Node("A15", isMax=True, value=14)
a16 = Node("A16", isMax=True, value=15)
a17 = Node("A17", isMax=True, value=16)
a18 = Node("A18", isMax=True, value=15)
a19 = Node("A19", isMax=True, value=17)
a20 = Node("A20", isMax=True, value=13)
a21 = Node("A21", isMax=True, value=15)

root.add_child(b)
root.add_child(c)
root.add_child(d)
b.add_child(e)
b.add_child(f)
c.add_child(g)
c.add_child(h)
d.add_child(i)
d.add_child(j)
d.add_child(k)
e.add_child(l)
e.add_child(m)
f.add_child(n)
g.add_child(o)
g.add_child(p)
h.add_child(q)
i.add_child(r)
i.add_child(s)
j.add_child(t)
k.add_child(u)
k.add_child(v)
l.add_child(w)
l.add_child(x)
m.add_child(y)
m.add_child(z)
n.add_child(a1)
n.add_child(a2)
n.add_child(a3)
o.add_child(a4)
o.add_child(a5)
o.add_child(a6)
p.add_child(a7)
q.add_child(a8)
q.add_child(a9)
q.add_child(a10)
r.add_child(a11)
s.add_child(a12)
s.add_child(a13)
s.add_child(a14)
t.add_child(a15)
t.add_child(a16)
u.add_child(a17)
u.add_child(a18)
v.add_child(a19)
v.add_child(a20)
v.add_child(a21)

score, path = minimax(root, depth=4)
print(f"Optimal Score: {score}")
print(f"Path: {' -> '.join(path)}")

score_ab, path_ab = minimax_alpha_beta(root, depth=4)
print(f"Optimal Score with αβ-Pruning: {score_ab}")
print(f"Path with αβ-Pruning: {' -> '.join(path_ab)}")


