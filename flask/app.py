from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from config import Config
from models.Bank import Bank
from models.Customer import Customer
from models.Employee import Employee
import MySQLdb.cursors
# import hashlib
# import bcrpt

# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(Config)
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():    
    return render_template('login.html')

@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'POST':
        emp_id = request.form.get('EmpUsername')
        employee = Employee.authenticate(mysql, emp_id)
        if employee:
            session['loggedin'] = True
            session['EmpUsername'] = emp_id
            return redirect(url_for('employee_dashboard'))
        else:
            flash('Invalid employee credentials', 'danger')
            return render_template('employee_login.html')
    return render_template('employee_login.html')

@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        # Get form data
        customer_id = request.form['customerUsername']

        # Authenticate customer (only customer_id check for now)
        account = Customer.authenticate(mysql, customer_id)

        if account:
            # Successful login, set up the session
            session['loggedin'] = True
            session['customer_id'] = account.customer_id
            session['customer_username'] = account.f_name  # Store first name

            flash('Login successful!', 'success')
            customer_data = Customer.read(mysql, session['customer_id'])
            # return render_template('customer_dashboard.html', customer=customer_data)  # Redirect to customer dashboard
            return redirect(url_for('customer_dashboard'))
        else:
            flash('Incorrect Customer ID!', 'danger')
    return render_template('customer_login.html')
#     if request.method == 'POST':
#         # Get form data
#         customer_id = request.form['customerUsername']
#         password = request.form['password']

#         # Authenticate customer
#         print(f"Attempting to authenticate customer: {customer_id}")
#         account = Customer.authenticate(mysql, customer_id, password)

#         if account:
#             # Successful login, set up the session
#             session['loggedin'] = True
#             session['customer_id'] = account['CUSTOMER_ID']
#             session['f_name'] = account.f_name
#             session['l_name'] = account.l_name  # or use any preferred identifier
#             flash('Login successful!', 'success')
#             return render_template('customer_dashboard.html', customer = account) # Redirect to a protected route
#         else:
#             flash('Incorrect Customer ID or Password!', 'danger')

#     # GET request or failed login attempt
#     return render_template('customer_login.html')
# @app.route('/customer_dashboard')

@app.route('/customer_dashboard', methods=['GET'])
def customer_dashboard():
    # Ensure user is logged in before accessing dashboard
    if 'loggedin' in session:
        customer_data = Customer.read(mysql, session['customer_id'])
        print("Customer Data:")
        if customer_data:

            return render_template('customer_dashboard.html', customer=customer_data)
            # return "found"
        else:
            flash('No customer found!', 'danger')
            return render_template('customer_login.html')  # Redirect if no customer found
    else:
        flash('Please log in first.', 'danger')
        return render_template('costumer_login.html') 


@app.route('/employee_dashboard', methods=['GET'])
def employee_dashboard():
    if 'loggedin' in session:
        employee_data = Employee.read(mysql, session['EmpUsername'])
        if employee_data:
            return render_template('employee_dashboard.html', employee=employee_data)
        else:
            flash('No employee found!', 'danger')
            return render_template('employee_login.html')
    else:
        flash('Please log in first.', 'danger')
        return render_template('employee_login.html')
@app.route('/search_cust', methods=['POST','GET'])
def search_cust():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        if customer_id:
            customer = Customer.search(mysql, customer_id)
            print("Data passed to template:", customer)
            if customer:
                return render_template('search_cust.html', customer=[customer])
    customer_data = Customer.read_all(mysql)
    return render_template("search_cust.html", customer = customer_data)

@app.route('/create_cust', methods=['POST', 'GET'])
def create_cust():
    if request.method == 'POST':
        password = request.form['password']
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        mobile_no = request.form['mobile_no']
        address = request.form['address']
        initial_balance = request.form['initial_balance']
        # account_type = request.form.get['account_type']
        Customer.create(mysql, password, f_name, l_name, mobile_no, address, initial_balance)
    return render_template('create_cust.html')

@app.route('/update_cust', methods=['POST', 'GET'])
def update_cust():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        password = request.form['password']
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        mobile_no = request.form['mobile_no']
        address = request.form['address']

        Customer.update(mysql, customer_id, password, f_name, l_name, mobile_no, address)

    return render_template('update_cust.html')
@app.route('/delete_cust', methods=['POST', 'GET'])
def delete_cust():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        Customer.delete(mysql, customer_id)
    return render_template('delete_cust.html')


@app.route('/loan', methods=['GET'])
# def loan():  
#     customer_id = request.args.get('customer_id')
#     customer = Customer(customer_id=customer_id)
#     loan_data = Customer.get_loan_details(mysql)  
#     if loan_data:
#         return render_template('loan.html', loan = loan_data)
#     else:
#         return jsonify({"message": "No loan details found for this customer"})
    
@app.route('/loan', methods=['GET'])
def loan():
    # Check if the user is logged in and `customer_id` is in the session
    if 'loggedin' in session and 'customer_id' in session:
        # customer_id = session['customer_id']  # Retrieve customer_id from session
        # customer = Customer(customer_id=customer_id)
        loan_data = Customer.get_loan_details(mysql, session['customer_id'])
        try:
            # Fetch loan details for the logged-in customer
            # loan_data = Customer.get_loan_details(mysql, customer_id)
            if loan_data:
                return render_template('loan.html', loan=loan_data)
            else:
                flash("No loan details found for this customer.", "warning")
                return redirect(url_for('customer_dashboard'))
        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred while retrieving loan details.", "danger")
            return redirect(url_for('login'))
    else:
        flash("Please log in to view loan details.", "danger")
        return redirect(url_for('customer_login'))







@app.route('/create_bank', methods=['GET', 'POST'])
def create_bank():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        address = request.form['address']
        Bank.create(name, city, address)
        flash("Bank created successfully!", "success")
        return redirect(url_for('index'))
    return render_template('create_bank.html')
def create_account():
    # your logic here
    return render_template('create_account.html')

@app.route('/view_bank/<int:code>')
def view_bank(code):
    bank = Bank.read(code)
    return render_template('view_bank.html', bank=bank)


if __name__ == "__main__":
    app.run(debug=True,port=8000)