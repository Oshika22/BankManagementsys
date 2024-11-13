def index():
    conn = mysql.connector.connect(
        host="localhost",  # MySQL server
        user="root",       # MySQL username
        password="abcd",  # MySQL password
        database="Bank_Management"   # Database name
    )
    
    # Create a cursor and execute query
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bank")  # Your table name
    
    # Fetch all results
    result = cursor.fetchall()
    
    # Convert result to list of dictionaries for JSON response
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in result]
    
    # Close connection
    cursor.close()
    conn.close()
    
    return jsonify(data)