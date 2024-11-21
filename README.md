
# Bank Management System

## Overview
The **Bank Management System** is a web-based application built using Flask and MySQL. It facilitates efficient banking operations through dedicated dashboards for employees and customers, offering functionalities such as customer management, secure authentication, and account access.

## Features

### Authentication
- **Secure Login**:
  - Employees use their Employee ID and password to access the system.
  - Customers log in using their Customer ID and password.
- **Role-Based Access**:
  - Employees manage customer data through their dashboard.
  - Customers can view account details and submit service requests.

### Employee Dashboard
- Add new customers to the system.
- Update existing customer details.
- Delete customer records.
- View the list of all customers.
- Search for customers by their Customer ID.
- Display employee-specific details on login.



## Technologies Used
- **Backend**: Flask (Python)
- **Database**: MySQL (Using `flask_mysqldb` and `MySQLdb.cursors`)
- **Frontend**: HTML, CSS, JavaScript

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server
- A virtual environment (recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd bank-management-system
   ```
3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up the database:
   - Create a MySQL database.
   - Import the provided SQL schema file into your database:
     ```bash
     mysql -u <username> -p <database_name> < schema.sql
     ```
6. Configure database credentials in `config.py`:
   ```python
   app.config['MYSQL_HOST'] = 'localhost'
   app.config['MYSQL_USER'] = 'your_username'
   app.config['MYSQL_PASSWORD'] = 'your_password'
   app.config['MYSQL_DB'] = 'your_database_name'
   ```
7. Run the application:
   ```bash
   flask run
   ```
8. Access the application in your browser:
   ```
   http://127.0.0.1:5000/
   ```

## Database Integration Code

### Libraries Used
```python
from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
```

### Configuration Example
```python
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'your_database_name'

mysql = MySQL(app)
```

### Query Example
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'employee_id' in request.form and 'password' in request.form:
        employee_id = request.form['employee_id']
        password = request.form['password']

        # Query database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employees WHERE employee_id = %s AND password = %s', (employee_id, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['name'] = account['name']
            return redirect('/dashboard')
        else:
            return 'Invalid credentials!'
    return render_template('login.html')
```

## Usage
1. **Employee Login**:
   - Access customer management features.
2. **Customer Login**:
   - View account details and request additional services.

## Future Enhancements
- Add email notifications for account updates or requests.
- Implement data visualization for better analytics in dashboards.
- Introduce mobile app support.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
- Developed by Oshika Sharma And Pranjali Yeotikar
- Frameworks and libraries: Flask, `flask_mysqldb`, `MySQLdb.cursors`
- Database: MySQL