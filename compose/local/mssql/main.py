import pyodbc

server = "10.0.1.156"
database = "xirux12"
username = "sicop"
password = "S1c0p2024+"
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER="
    + server
    + ";PORT=8443;DATABASE="
    + database
    + ";UID="
    + username
    + ";PWD="
    + password
    + ";Encrypt=no",
)
cursor = conn.cursor()
cursor.execute("SELECT @@VERSION")
print(cursor.fetchone()[0])
