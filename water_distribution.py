import networkx as nx
import matplotlib.pyplot as plt

# Defining the  city nodes with attributes
city_nodes = {
    'A': {'population_density': 100, 'proximity': 5, 'infrastructure': 7},
    'B': {'population_density': 70, 'proximity': 3, 'infrastructure': 5},
    'C': {'population_density': 50, 'proximity': 8, 'infrastructure': 6},
    'D': {'population_density': 90, 'proximity': 6, 'infrastructure': 9},
    'E': {'population_density': 60, 'proximity': 4, 'infrastructure': 4},
}

# Creating a network graph of the city
city_network = nx.Graph()

# Adding nodes with weights representing priority (higher density, lower proximity, and better infrastructure readiness)
for node, data in city_nodes.items():
    priority_score = data['population_density'] * (10 - data['proximity']) * data['infrastructure']
    city_network.add_node(node, priority=priority_score)

# Defining edges with weights (cost of laying pipes between nodes)
edges = [
    ('A', 'B', 10),
    ('A', 'C', 20),
    ('B', 'C', 15),
    ('B', 'D', 25),
    ('C', 'D', 30),
    ('D', 'E', 20),
]

# Adding edges with costs to the graph
for edge in edges:
    city_network.add_edge(edge[0], edge[1], cost=edge[2])

# Function to apply greedy approach for network expansion
def greedy_water_distribution(city_network):
    selected_edges = []
    total_cost = 0

    # Sort edges by priority of nodes and cost of connection
    sorted_edges = sorted(
        city_network.edges(data=True),
        key=lambda x: (city_network.nodes[x[0]]['priority'] + city_network.nodes[x[1]]['priority']) / 2 - x[2]['cost'],
        reverse=True,
    )

    # Greedy selection 
    for u, v, data in sorted_edges:
        if not nx.has_path(city_network, u, v):
            selected_edges.append((u, v, data['cost']))
            total_cost += data['cost']
            city_network.add_edge(u, v, cost=data['cost'])

    return selected_edges, total_cost

# Applying the greedy algorithm to find the optimal water distribution network
optimal_edges, minimal_cost = greedy_water_distribution(city_network)

#  selected edges and total cost
print("Optimal Water Distribution Network (Selected Edges with Cost):")
for edge in optimal_edges:
    print(f"Connection from {edge[0]} to {edge[1]} with cost {edge[2]}")
print(f"Total Cost of the Water Distribution Network: {minimal_cost}")

# Visualize the network
pos = nx.spring_layout(city_network)
nx.draw(city_network, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=12)
labels = nx.get_edge_attributes(city_network, 'cost')
nx.draw_networkx_edge_labels(city_network, pos, edge_labels=labels)
plt.show()
