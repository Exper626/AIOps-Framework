
from pymongo import MongoClient
from py2neo import Graph, Node, Relationship
import pprint

# MongoDB Connection
def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["company_attendance"]
    return db["attendance"]

# Neo4j Connection
def connect_neo4j():
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "Manith@123"))  # Replace with your credentials

    return graph

# Transfer MongoDB data to Neo4j
def transfer_data_to_neo4j():
    # Connect to MongoDB and Neo4j
    mongo_collection = connect_mongo()
    neo4j_graph = connect_neo4j()

    # Fetch all attendance records from MongoDB
    records = mongo_collection.find()

    for record in records:
        employee_id = record["employee_id"]
        employee_name = record["name"]
        date = record["date"]
        status = "Present" if record["status"] else "Absent"

        # Create Employee Node
        employee_node = Node("Employee", id=employee_id, name=employee_name)
        neo4j_graph.merge(employee_node, "Employee", "id")

        # Create Date Node
        date_node = Node("Date", date=date)
        neo4j_graph.merge(date_node, "Date", "date")

        # Create Relationship
        attendance_relationship = Relationship(employee_node, "ATTENDED", date_node, status=status)
        neo4j_graph.create(attendance_relationship)

    print("Data transferred to Neo4j successfully!")

# Visualize the Graph (Optional)
def visualize_graph():
    neo4j_graph = connect_neo4j()

    # Example query to fetch employees and their attendance status
    query = """
    MATCH (e:Employee)-[r:ATTENDED]->(d:Date)
    RETURN e.name AS employee, d.date AS date, r.status AS status
    """
    
    result = neo4j_graph.run(query)
    
    # Display results
    for record in result:
        print(f"Employee: {record['employee']}, Date: {record['date']}, Status: {record['status']}")

# Main
if __name__ == "__main__":
    transfer_data_to_neo4j()
    visualize_graph()
