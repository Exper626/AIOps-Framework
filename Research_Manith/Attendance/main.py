import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, DateTime, select, text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import sqlite3
import ollama
from sqlalchemy import text
# Database setup

Base = declarative_base()

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    employee_id = Column(String)
    employee_name = Column(String)
    department = Column(String)
    date_time = Column(DateTime)
    status = Column(String)  # in / out

engine = create_engine('sqlite:///attendance.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

st.title("🕒 Employee Attendance System")

# Tabs for CRUD and LLM Query
tab1, tab2 = st.tabs(["Manage Attendance", "Ask via AI"])

with tab1:
    st.header("Add / Update / Delete Attendance")

    employee_id = st.text_input("Employee ID")
    employee_name = st.text_input("Employee Name")
    department = st.text_input("Department")


    date = st.date_input("Date", datetime.now().date())
    time = st.time_input("Time", datetime.now().time())
    date_time = datetime.combine(date, time)


    status = st.selectbox("Status", ["in", "out"])

    if st.button("Add Attendance"):
        new_record = Attendance(
            employee_id=employee_id,
            employee_name=employee_name,
            department=department,
            date_time=date_time,
            status=status
        )
        session.add(new_record)
        session.commit()
        st.success("Record added!")

    st.subheader("Delete Attendance by ID")
    delete_id = st.text_input("Enter ID to delete")
    if st.button("Delete"):
        record = session.query(Attendance).filter_by(id=delete_id).first()
        if record:
            session.delete(record)
            session.commit()
            st.success("Record deleted")
        else:
            st.error("Record not found")

    st.subheader("All Records")
    rows = session.query(Attendance).all()
    st.table([{
        'ID': r.id,
        'Employee ID': r.employee_id,
        'Name': r.employee_name,
        'Department': r.department,
        'DateTime': r.date_time,
        'Status': r.status
    } for r in rows])

with tab2:
    st.header("Ask Questions About Employee Attendance")
    user_query = st.text_area("Ask your question:")

    if st.button("Ask"):
        prompt = f"""You are a helpful assistant. Given the user query, write an SQL SELECT statement for SQLite to fetch from the 'attendance' table. Only return the SQL query, no explanation.
        
        Example:
        Q: Show me all 'in' attendances from the IT department.
        A: SELECT * FROM attendance WHERE status = 'in' AND department = 'IT';

        
        Here is the schema:
        - id (integer)
        - employee_id (text)
        - employee_name (text)
        - department (text)
        - date_time (datetime)
        - status (text, values: 'in', 'out')



        Now, here is the user query:
        {user_query}
        """
        response = ollama.chat(model='llama3.2:1b', messages=[{"role": "user", "content": prompt}])
        sql_query = response['message']['content'].strip('` \n')
        
        st.code(sql_query, language='sql')

        try:
            with engine.connect() as conn:
                result = conn.execute(text(sql_query))
                st.dataframe([dict(row._mapping) for row in result])
        except Exception as e:
            st.error(f"Error executing SQL: {e}")
