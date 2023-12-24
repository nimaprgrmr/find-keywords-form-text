import pyodbc

# Replace these with your actual server and database details
server = '.\SqlServer2019'
database = 'Paydar'
username = 'sa'
password = 'PAYA+master'
table_name = 'TrsReconcileDtl'

# Establish the connection
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(connection_string)

# Create a cursor from the connection
cursor = connection.cursor()

# Now you can execute SQL queries using the cursor
try:
    # Use the actual table name in your query
    cursor.execute(f'SELECT * FROM {table_name}')

    # Fetch the results, for example:
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as e:
    print(f"Error: {e}")

# Don't forget to close the cursor and connection when done
cursor.close()
connection.close()