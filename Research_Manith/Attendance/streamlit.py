import streamlit as st
from pymongo import MongoClient
import pprint
import ollama
from neo4j import GraphDatabase
import re


# Connect to Neo4j (update credentials as needed)
NEO4J_URI = "bolt://localhost:7689"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Manith@12345"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def run_cypher_query(cypher_query):
    try:
        with driver.session() as session:
            result = session.run(cypher_query)
            return [record.data() for record in result]
    except Exception as e:
        return f"Cypher query error: {e}"




def ollamaModelConnection(prompt):
    """Send prompt to Ollama model and return raw Cypher query"""
    try:
        response = ollama.chat(
            model="deepseek-r1:latest",  # Replace with your model's name
            messages=[
                {
#                     "role": "system",
#                     "content": (
#             "You are a helpful assistant that converts natural language questions into Cypher queries for a Neo4j graph. "
#             "Only return raw Cypher query output (no markdown/code block, no explanation). "
#             "Your output goes directly to a graph database (Neo4j), so accuracy and formatting are crucial."
#             "these are the records : _id,  employee_id, name, department, date, check_in, check_out, status "
#             "For example :  HR ---> relationshp : works in, Bob ---> relationshp : attended ----> 3"
#             "For example : Department node has <elementId>	4:4f6324bd-cc71-48ae-85aa-4fff81a8659b:1 <id>1 name HR"
#             "For example : Employee node has<elementId>	4:4f6324bd-cc71-48ae-85aa-4fff81a8659b:5 <id>5 id E004 name	David"
# "For example : Attendance node has <elementId>	4:4f6324bd-cc71-48ae-85aa-4fff81a8659b:15 <id>	15 date 4 inTime	09:00 month 04 outTime	17:00"
#                     )

        "role": "system",
"content": ("You are a helpful assistant that converts natural language questions into Cypher queries for a Neo4j graph. "
                    "Only return raw Cypher query output. Do not include explanations, markdown, or formatting. "
                    "The Cypher will be sent directly to the Neo4j database, so accuracy is critical. "
                    "Schema information: \n"
                    "- Node Types:\n"
                    "    * Department: { name }\n"
                    "    * Employee: { id, name }\n"
                    "    * Attendance: { date, inTime, outTime, month }\n"
                    "- Relationships:\n"
                    "    * (e:Employee)-[:WORKS_IN]->(d:Department)\n"
                    "    * (e:Employee)-[:ATTENDED]->(a:Attendance)\n"
"MATCH (e:Employee {name: 'Alice'})-[:attended]->(a:Attendance) RETURN a.date, a.inTime, a.outTime, a.month"
                )
                    
                },
                {"role": "user", "content": prompt}
            ]
        )

        raw = response['message']['content'].strip()

        # If model added explanation or thinking, extract query from code block
        # Look for content inside triple backticks (```cypher ... ```)
        match = re.search(r"```(?:cypher)?\s*([\s\S]+?)```", raw, re.IGNORECASE)
        if match:
            query = match.group(1).strip()
        else:
            # If no triple backticks but query starts somewhere in the middle
            # Try to find first MATCH/CREATE/etc. and extract from there
            match = re.search(r"(?i)\b(MATCH|CREATE|MERGE|RETURN|CALL|WITH|OPTIONAL\s+MATCH)\b[\s\S]+", raw)
            query = match.group(0).strip() if match else raw

        # Final sanity check
        if not query.upper().startswith(("MATCH", "CREATE", "MERGE", "RETURN", "CALL", "WITH", "OPTIONAL MATCH")):
            raise ValueError(f"Model output may not be a valid Cypher query:\n{query}")

        print("The query is : ", query)
        return query

    except Exception as e:
        return f"Error communicating with Ollama model: {e}"


# MongoDB connection
def connectToMongoDB():
    """Connect to MongoDB and initialize collection"""
    global attendance_collection

    client = MongoClient("mongodb://localhost:27017/")  ################ Change to your MongoDB URI
    db = client["company_attendance"]
    attendance_collection = db["attendance"]


def insert(_id: str, employee_id: str, name: str, department: str, date: str, check_in: str, check_out: str, status: bool):
    """Insert a single record to MongoDB"""
    global attendance_collection

    record = { "_id": _id, "employee_id": employee_id, "name": name, "department": department, "date": date, 
              "check_in":  check_in, "check_out": check_out, "status": status }

    try:
        attendance_collection.insert_one(record)
        return "Data inserted successfully!"
    except Exception as e:
        return f"Insert error: {e}"


def update(_id: str, update_fields: dict):
    """Update a record in MongoDB by _id"""
    global attendance_collection

    result = attendance_collection.update_one({"_id": _id}, {"$set": update_fields})
    if result.modified_count > 0:
        return "Record updated successfully."
    else:
        return "No record was updated. Check if the _id exists."


def delete(_id: str):
    """Delete a record from MongoDB by _id"""
    global attendance_collection

    result = attendance_collection.delete_one({"_id": _id})
    if result.deleted_count > 0:
        return "Record deleted successfully."
    else:
        return "No record was deleted. Check if the _id exists."


def get(filter_query: dict = {}):
    """Retrieve and print records from MongoDB"""
    global attendance_collection

    results = attendance_collection.find(filter_query)
    return list(results)



#############  User Interface ---------------------------------------------------------------------------------

# Streamlit UI
st.title("Employee Attendance System")
connectToMongoDB()



st.header("Natural Language to Cypher Query (Ollama)")
nl_query = st.text_area("Type your query in natural language:", "")



if st.button("Generate & Run Cypher Query"):
    if nl_query.strip():
        cypher_query = ollamaModelConnection(nl_query)
        st.subheader("Generated Cypher Query:")
        st.code(cypher_query, language='cypher')
        
        result = run_cypher_query(cypher_query)

        # Convert result to pretty-printed string
        import pprint
        result_text = pprint.pformat(result, indent=2)

        # Display the result in a read-only text area
        st.text_area("Query Result", result_text, height=300, disabled=True)

    else:
        st.warning("Please enter a query first.")





if "show_add" not in st.session_state:
    st.session_state.show_add = False
if "show_view" not in st.session_state:
    st.session_state.show_view = False
if "show_update" not in st.session_state:
    st.session_state.show_update = False
if "show_delete" not in st.session_state:
    st.session_state.show_delete = False


def toggle_section(section_name):
    for section in ["show_add", "show_view", "show_update", "show_delete"]:
        if section == section_name:
            st.session_state[section] = not st.session_state[section]
        else:
            st.session_state[section] = False


if st.button('Add Attendance'):
    toggle_section("show_add")
if st.button('View Attendance Records'):
    toggle_section("show_view")
if st.button('Update Attendance'):
    toggle_section("show_update")
if st.button('Delete Attendance'):
    toggle_section("show_delete")


# Show Add Attendance form if toggled
if st.session_state.show_add:
    st.header("Add Attendance Record")
    with st.form(key='insert_form'):
        #_id = st.text_input("Record ID (_id)")
        employee_id = st.text_input("Employee ID")
        name = st.text_input("Employee Name")
        department = st.text_input("Department")
        date = st.date_input("Date")
        check_in = st.time_input("Check-In Time")
        check_out = st.time_input("Check-Out Time")
        status = st.selectbox("Status", ["present", "absent"])

        submit_button = st.form_submit_button("Add Record")
        if submit_button:
            status_bool = True if status == "present" else False
            msg = insert(_id, employee_id, name, department, date.strftime("%Y-%m-%d"), check_in.strftime("%H:%M"), check_out.strftime("%H:%M"), status_bool)
            st.success(msg)


# Show View Attendance Records if toggled
if st.session_state.show_view:
    st.header("View Attendance Records")
    attendance_data = get()
    if attendance_data:
        st.write("Records:")
        for record in attendance_data:
            st.write(record)


# Show Update Attendance form if toggled
if st.session_state.show_update:
    st.header("Update Attendance Record")
    with st.form(key='update_form'):
        update_id = st.text_input("Record ID to Update")
        update_check_out = st.time_input("New Check-Out Time")
        update_status = st.selectbox("New Status", ["present", "absent"])

        update_button = st.form_submit_button("Update Record")
        if update_button:
            status_bool = True if update_status == "present" else False
            msg = update(update_id, {"check_out": update_check_out.strftime("%H:%M"), "status": status_bool})
            st.success(msg)


# Show Delete Attendance form if toggled
if st.session_state.show_delete:
    st.header("Delete Attendance Record")
    with st.form(key='delete_form'):
        delete_id = st.text_input("Record ID to Delete")
        delete_button = st.form_submit_button("Delete Record")
        if delete_button:
            msg = delete(delete_id)
            st.success(msg)

else:
    st.write("Click a button above to perform a task.")
