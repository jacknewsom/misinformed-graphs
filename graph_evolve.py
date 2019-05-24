import random
from nodes import Instructor, Student

n_students = 50

# number of instructor-student connections
nisc = 5

# number of student-student connections
nssc = 40

# number of simulation timesteps
timesteps = 20

prof = Instructor(0)
students = [Student(i) for i in range(n_students)]

# randomly select 'nisc' students from total 'n_students'
isc = []
for i in random.sample(range(n_students), nisc):
    students[i].add_neighbor(prof)
    isc.append((prof, students[i]))

# randomly select 'nssc' pairs of students from total 'n_students'
j, k = 0, 0
pairs = []
for i in range(nssc):
    while j == k or (students[j], students[k]) in pairs or (students[k], students[j]) in pairs:
        j = int(random.random() * n_students)
        k = int(random.random() * n_students)

    students[j].add_neighbor(students[k])
    students[k].add_neighbor(students[j])

    pairs.append((students[j], students[k]))

import networkx as nx
import matplotlib.pyplot as plt

nodes = [prof] + students
edges = isc + pairs

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

beliefs = [i.belief for i in nodes]

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                       vmin=-1, vmax=1, node_color=beliefs, 
                       node_size=100)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=edges)

plt.show()

for t in range(timesteps):
    new_beliefs = []
    for s in students:
        new_beliefs.append(s.collect_beliefs())
    for s, b in zip(students, new_beliefs):
        s.update_belief(b)

beliefs = [i.belief for i in nodes]

nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                       vmin=-1, vmax=1, node_color=beliefs, 
                       node_size=100)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=edges)
plt.show()


