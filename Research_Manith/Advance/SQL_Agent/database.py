import sqlite3

connection=sqlite3.connect("student.db")
cursor=connection.cursor()

table_info = """
    Create table STUDENT(NAME VARCHAR(25), SUBJECT VARCHAR(25), GRADE VARCHAR(25), MARKS INT);
"""
cursor.execute(table_info)

cursor.execute('''Insert Into STUDENT values('Manith','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Rob','Data Science','B',70)''')
cursor.execute('''Insert Into STUDENT values('Bob','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('John','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Peter','DEVOPS','A',95)''')

print("The inserted records are")

data=cursor.execute('''Select * from STUDENT''')

for row in data:
    print(row)

connection.commit()
connection.close()