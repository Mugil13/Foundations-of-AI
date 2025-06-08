# Session 8: Bayesian Network and Joint Probability Distribution

import networkx as nx
import matplotlib.pyplot as plt

# 1) Constructing the DAG
bn_graph = nx.DiGraph()

# Add nodes for each variable in the Bayesian Network
bn_graph.add_nodes_from(["IQ Level", "Exam Level", "Marks", "Aptitude Score", "Admission"])

# Add directed edges based on the specified dependencies
edges = [
    ("Exam Level", "Marks"),
    ("Marks", "Admission"),
    ("IQ Level", "Marks"),
    ("IQ Level", "Aptitude Score")
]
bn_graph.add_edges_from(edges)

plt.figure(figsize=(10, 8))
pos = {
    "IQ Level": (0, 1),
    "Exam Level": (1, 1),
    "Marks": (0.5, 0),
    "Aptitude Score": (0, 0.5),
    "Admission": (0.5, -0.5)
}
nx.draw(
    bn_graph, pos, with_labels=True, node_size=8000, node_color="skyblue",
    font_size=11, font_weight="bold", arrows=True, edge_color="black", linewidths=3
)

plt.title("Bayesian Network Structure", fontsize=18, fontweight='bold')
plt.grid(False)
plt.axis('off')
plt.show()

# 2) Conditional Probability Tables (CPT)
P_IQ = {0: 0.8, 1: 0.2}  # IQ Level
P_Exam = {0: 0.7, 1: 0.3}  # Exam Level

P_Marks_given_IQ_Exam = {
    (0, 0): {0: 0.6, 1: 0.4},
    (0, 1): {0: 0.1, 1: 0.9},
    (1, 0): {0: 0.5, 1: 0.5},
    (1, 1): {0: 0.8, 1: 0.2}
}

P_Aptitude_given_IQ = {
    0: {0: 0.75, 1: 0.25},
    1: {0: 0.4, 1: 0.6}
}

P_Admission_given_Marks = {
    0: {0: 0.6, 1: 0.4},
    1: {0: 0.9, 1: 0.1}
}

# Function to print CPT
def print_cpt(table, variable_name, given_vars=None):
    print(f"\nConditional Probability Table for {variable_name}")
    if given_vars:
        print(f"Given {given_vars}:")
    if isinstance(list(table.values())[0], dict):
        # Nested dictionary structure
        for condition, outcomes in table.items():
            cond_str = f"{condition}" if isinstance(condition, tuple) else f"{given_vars}={condition}"
            for outcome, prob in outcomes.items():
                print(f"P({variable_name}={outcome} | {cond_str}) = {prob}")
    else:
        for outcome, prob in table.items():
            print(f"P({variable_name}={outcome}) = {prob}")

print("\nConditional Probability Tables (CPTs):")
print_cpt(P_IQ, "IQ Level")
print_cpt(P_Exam, "Exam Level")
print_cpt(P_Marks_given_IQ_Exam, "Marks", given_vars="IQ Level and Exam Level")
print_cpt(P_Aptitude_given_IQ, "Aptitude Score", given_vars="IQ Level")
print_cpt(P_Admission_given_Marks, "Admission", given_vars="Marks")

# 3) User Input for Joint Probability Distribution Calculation
print("\nPlease enter the values for the following variables:")
iq = int(input("IQ Level (0 for False, 1 for True): "))
exam = int(input("Exam Level (0 for False, 1 for True): "))
marks = int(input("Marks (0 for False, 1 for True): "))
aptitude = int(input("Aptitude Score (0 for False, 1 for True): "))
admission = int(input("Admission (0 for False, 1 for True): "))

# Function for Joint Probability Distribution
def joint_probability(iq, exam, marks, aptitude, admission):
    P_I = P_IQ[iq]
    P_E = P_Exam[exam]
    P_M_given_IE = P_Marks_given_IQ_Exam[(iq, exam)][marks]
    P_A_given_I = P_Aptitude_given_IQ[iq][aptitude]
    P_AD_given_M = P_Admission_given_Marks[marks][admission]
    
    # Joint probability is the product of all conditional probabilities
    return P_I * P_E * P_M_given_IE * P_A_given_I * P_AD_given_M

probability = joint_probability(iq, exam, marks, aptitude, admission)
print(f"\nJoint Probability P(IQ={iq}, Exam={exam}, Marks={marks}, Aptitude={aptitude}, Admission={admission}):", probability)