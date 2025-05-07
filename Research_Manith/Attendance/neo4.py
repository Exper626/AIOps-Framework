
from neo4j import GraphDatabase

# Replace these with your actual credentials
NEO4J_URI = "bolt://localhost:7689"  # or "neo4j+s://<hostname>:<port>" for Aura/Cloud
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "Manith@12345"

# Create a driver instance
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# Function to run a simple query
def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Connected to Neo4j!' AS message")
        for record in result:
            print(record["message"])

# Test the connection
test_connection()

# Close the driver when done
driver.close()
