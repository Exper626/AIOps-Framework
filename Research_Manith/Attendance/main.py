import streamlit as st
from pymongo import MongoClient
import pprint


# MongoDB connection
def connectToMongoDB():
    """Connect to MongoDB and initialize collection"""
    global attendance_collection

    client = MongoClient("mongodb://localhost:27017/")  # Change to your MongoDB URI
    db = client["company_attendance"]
    attendance_collection = db["attendance"]


# Insert a record into MongoDB
def insert(_id: str, employee_id: str, name: str, department: str, date: str, check_in: str, check_out: str, status: bool):
    """Insert a single record to MongoDB"""
    global attendance_collection

    record = {
        "_id": _id,
        "employee_id": employee_id,
        "name": name,
        "department": department,
        "date": date,
        "check_in": check_in,
        "check_out": check_out,
        "status": status
    }

    try:
        attendance_collection.insert_one(record)
        return "Data inserted successfully!"
    except Exception as e:
        return f"Insert error: {e}"


# Update a record in MongoDB by _id
def update(_id: str, update_fields: dict):
    """Update a record in MongoDB by _id"""
    global attendance_collection

    result = attendance_collection.update_one({"_id": _id}, {"$set": update_fields})
    if result.modified_count > 0:
        return "Record updated successfully."
    else:
        return "No record was updated. Check if the _id exists."


# Delete a record from MongoDB by _id
def delete(_id: str):
    """Delete a record from MongoDB by _id"""
    global attendance_collection

    result = attendance_collection.delete_one({"_id": _id})
    if result.deleted_count > 0:
        return "Record deleted successfully."
    else:
        return "No record was deleted. Check if the _id exists."


# Retrieve and print records from MongoDB
def get(filter_query: dict = {}):
    """Retrieve and print records from MongoDB"""
    global attendance_collection

    results = attendance_collection.find(filter_query)
    return list(results)



#--------------------------------------------------------------------------------------------------------------

# Streamlit UI
st.title("Employee Attendance System")

# Connect to MongoDB
connectToMongoDB()

# Initialize session state for toggling visibility
if "show_add" not in st.session_state:
    st.session_state.show_add = False
if "show_view" not in st.session_state:
    st.session_state.show_view = False
if "show_update" not in st.session_state:
    st.session_state.show_update = False
if "show_delete" not in st.session_state:
    st.session_state.show_delete = False


# Toggle function to show and hide sections
def toggle_section(section_name):
    for section in ["show_add", "show_view", "show_update", "show_delete"]:
        if section == section_name:
            st.session_state[section] = not st.session_state[section]
        else:
            st.session_state[section] = False


# Buttons to toggle functionality
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
        _id = st.text_input("Record ID (_id)")
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
