import streamlit as st
import sqlite3
import requests
import ollama

DB_FILE = "student.db"

def ask_ollama(question):
    
    prompt =  f"""You are a helpful assistant that only returns raw SQL commands.
              You are not supposed to output any output other than SQL commands.
              The database structure looks like this
              table STUDENT(NAME VARCHAR(25), SUBJECT VARCHAR(25), GRADE VARCHAR(25), MARKS INT). 
              User asked: {question}.\nReturn only the SQL query to execute."""

    response = ollama.chat(model="llama3.2:1b", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]


def run_sql_query(sql):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description] if cur.description else []
        conn.close()
        return headers, rows
    except sqlite3.Error as e:
        conn.close()
        return [], [[f"SQL Error: {e}"]]


st.title("Student Grade Assistant Agent")
question = st.text_input("Ask a question about students :")

if st.button("Submit") and question:
    
    st.info("Sending to LLM...")
    sql_query = ask_ollama(question)
    st.code(sql_query, language="sql")

    st.info("Running SQL query...")
    headers, results = run_sql_query(sql_query)

    if headers:
        st.table([headers] + results)
    else:
        st.write(results[0][0]) 
