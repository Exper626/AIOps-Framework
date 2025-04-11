
import matplotlib.pyplot as plt
import networkx as nx
from py2neo import Graph

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "Manith@123"))

# Query to get employee and attendance data
query = """
MATCH (e:Employee)-[r:ATTENDED]->(d:Date)
RETURN e.name AS employee, d.date AS date, r.status AS status
"""
result = graph.run(query)

# Create a NetworkX graph
G = nx.Graph()

# Add nodes and relationships (edges) from the result
for record in result:
    employee = record["employee"]
    date = record["date"]
    status = record["status"]
    
    # Add nodes
    G.add_node(employee, type="Employee")
    G.add_node(date, type="Date")
    
    # Add relationship (edge)
    G.add_edge(employee, date, status=status)

# Draw the graph
pos = nx.spring_layout(G)  # Positioning layout
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=12)
edge_labels = nx.get_edge_attributes(G, "status")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Show the plot
plt.title("Employee Attendance Graph")
plt.show()
