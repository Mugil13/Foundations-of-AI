# Session 7: Proof Procedures in Propositional Logic

# Class Clause represents a definite clause with a head and a body of atoms
class Clause(object):    
    def __init__(self, head, body=[]):
        # Clause with atom head and list of atoms body
        self.head = head
        self.body = body 

class Askable(object):
    # Represents atoms that can be queried or asked
    def __init__(self, atom):
        self.atom = atom

class KB:
    # A knowledge base consists of a set of clauses and askables
    def __init__(self, statements=[]):
        self.statements = statements
        self.clauses = []  
        self.askables = []  
        self.atom_to_clauses = {}
        self.askable_values = {}  # Stores responses to askable atoms
        for s in statements:
            if isinstance(s, Clause):
                self.add_clause(s)
            elif isinstance(s, Askable):
                self.askables.append(s.atom)

    # Adding new clauses to the knowledge base
    def add_clause(self, c):
        self.clauses.append(c)
        if c.head not in self.atom_to_clauses:
            self.atom_to_clauses[c.head] = []
        self.atom_to_clauses[c.head].append(c)

    # Returning the list of clauses where the atom a is the head
    def clauses_for_atom(self, a):
        return self.atom_to_clauses.get(a, [])

    # Asking the user about askable atoms
    def ask_user(self, atom):
        if atom not in self.askable_values:
            response = input(f"Is '{atom}' true? (yes/no): ").strip().lower()
            self.askable_values[atom] = (response == "yes")
        return self.askable_values[atom]

    # Bottom-Up Proof
    def bottom_up_proof(self):
        known_atoms = set()
        added = True
        while added:
            added = False
            for clause in self.clauses:
                if all(b in known_atoms for b in clause.body) and clause.head not in known_atoms:
                    known_atoms.add(clause.head)
                    added = True
        return known_atoms

    # Top-Down Proof
    def prove(self, goal):
        def recursive_prove(goals, known_atoms):
            if not goals:
                return True
            current_goal = goals[0]
            if current_goal in known_atoms:
                return recursive_prove(goals[1:], known_atoms)
            if current_goal in self.askables:
                if self.ask_user(current_goal):
                    known_atoms.add(current_goal)
                    return recursive_prove(goals[1:], known_atoms)
                else:
                    return False
            for clause in self.clauses_for_atom(current_goal):
                if recursive_prove(clause.body + goals[1:], known_atoms):
                    known_atoms.add(current_goal)
                    return True
            return False

        return recursive_prove(goal, set())

# Expanded Knowledge Base with Askable atoms
expanded_KB = KB([
    Clause('a', ['b', 'c']),
    Clause('b', ['d', 'e']),
    Clause('b', ['g', 'e']),
    Clause('c', ['e']),
    Clause('d'),
    Clause('e'),    
    Clause('f', ['a', 'g'])
])

# Bottom-up proof
consequence_set = expanded_KB.bottom_up_proof()
print("Bottom-up Proof Consequence Set:", consequence_set)

# Top-down proof for different goals
goal_1 = ['a']
goal_2 = ['b']
goal_3 = ['f']
goal_4 = ['g']
goal_5 = ['h']

is_provable_1 = expanded_KB.prove(goal_1)
is_provable_2 = expanded_KB.prove(goal_2)
is_provable_3 = expanded_KB.prove(goal_3)
is_provable_4 = expanded_KB.prove(goal_4)
is_provable_5 = expanded_KB.prove(goal_5)

print(f"Top-down Proof for goal {goal_1}: {is_provable_1}")
print(f"Top-down Proof for goal {goal_2}: {is_provable_2}")
print(f"Top-down Proof for goal {goal_3}: {is_provable_3}")
print(f"Top-down Proof for goal {goal_4}: {is_provable_4}")
print(f"Top-down Proof for goal {goal_5}: {is_provable_5}")