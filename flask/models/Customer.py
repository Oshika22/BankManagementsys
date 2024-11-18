# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_mysqldb import MySQL
# from config import Config
# import MySQLdb.cursors
# from werkzeug.security import check_password_hash, generate_password_hash

# app = Flask(__name__)

# app.config.from_object(Config)
# mysql = MySQL(app)

# class Customer:
#     def __init__(self, customer_id, name, email, phone):
#         self.customer_id = customer_id
#         self.name = name
#         self.email = email
#         self.phone = phone

#     @classmethod 
#     def authenticate(self, customer_id, password):
#         # Query to check if the customer exists and verify the password
#         cur = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         # cur = mysql.connection.cursor()
#         cur.execute('SELECT * FROM CUSTOMER WHERE CUSTOMER_ID = %s', (customer_id,))
#         account = cur.fetchone()
#         cur.close()
#         if account and check_password_hash(account['PASSWORD'], password):
#             # Password matches; return account info
#             return account
#         return None 
#     @classmethod
#     def read(self, customer_id):
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM CUSTOMER WHERE CUSTOMER_ID = %d",[customer_id])
#         customer_data = cur.fetchone()
#         cur.close()
#         return customer_data

from flask import current_app
from werkzeug.security import check_password_hash
import MySQLdb.cursors


class Customer:
    def __init__(self, customer_id=None, f_name=None, l_name=None, mobile_no=None, address = None, password = None):
        self.customer_id = customer_id
        self.f_name = f_name
        self.l_name = l_name
        self.mobile_no = mobile_no
        self.address = address
        self.password = password

    @classmethod
    def _execute_query(cls, mysql, query, params=None, fetchone=True):
        """Helper method to execute a database query."""
        # mysql = current_app.extensions['mysql']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Execute the query
        cur.execute(query, params)
        
        # Fetch data for read operations
        if fetchone:
            result = cur.fetchone()
        else:
            result = cur.fetchall()
        
        cur.close()
        return result

    @classmethod
    def read(cls, mysql, customer_id):
        query = "SELECT * FROM CUSTOMER WHERE CUSTOMER_ID = %s"
        customer_data = cls._execute_query(mysql, query, (customer_id,))
        if customer_data:
            return cls(
                customer_id = customer_data['CUSTOMER_ID'],
                f_name = customer_data['F_NAME'],
                l_name = customer_data.get('L_Name'),  
                mobile_no = customer_data['MOBILE_NO'],
                address = customer_data['ADDRESS'],
                password = customer_data['PASSWORD']
            )
        return None 
    @classmethod
    def read_all(cls, mysql):
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  # Use DictCursor
            query = """SELECT c.CUSTOMER_ID, c.F_NAME, c.L_NAME, c.MOBILE_NO, c.ADDRESS, 
                a.ACCOUNT_NO, a.BALANCE FROM CUSTOMER c LEFT JOIN ACCOUNT a ON c.CUSTOMER_ID = a.CUSTOMER_ID"""
            cur.execute(query)
            results = cur.fetchall()
            
            #Convert each row into a Customer object
            # customers = [
            #     cls(
            #         customer_id=row['CUSTOMER_ID'],
            #         f_name=row['F_NAME'],
            #         l_name=row['L_NAME'],
            #         mobile_no=row['MOBILE_NO'],
            #         address=row['ADDRESS'],
                    
            #     )
            #     for row in results
            # ]
            customers = [
                {
                    'customer_id': row['CUSTOMER_ID'],
                    'f_name': row['F_NAME'],
                    'l_name': row['L_NAME'],
                    'mobile_no': row['MOBILE_NO'],
                    'address': row['ADDRESS'],
                    'account_no': row['ACCOUNT_NO'],
                    'balance': row['BALANCE']
                }
                for row in results
            ]
            return  customers
        except Exception as e:
            print(f"Error reading from database: {e}")
            return ["error"]
        finally:
            cur.close()
    @classmethod
    def search(cls, mysql, customer_id):
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  # Use DictCursor
            query = """ SELECT c.CUSTOMER_ID, c.F_NAME, c.L_NAME, c.MOBILE_NO, c.ADDRESS, 
           a.ACCOUNT_NO, a.BALANCE
           FROM CUSTOMER c
           LEFT JOIN ACCOUNT a ON c.CUSTOMER_ID = a.CUSTOMER_ID
           WHERE c.CUSTOMER_ID = %s"""
            cur.execute(query, (customer_id,))
            result = cur.fetchone()
            if not result:
                print(f"No customer found for ID: {customer_id}")
                return None 
            customer = {
                'customer_id': result['CUSTOMER_ID'],
                'f_name': result['F_NAME'],
                'l_name': result['L_NAME'],
                'mobile_no': result['MOBILE_NO'],
                'address': result['ADDRESS'],
                'account_no': result.get('ACCOUNT_NO'),  # Use get() to handle possible None values
                'balance': result.get('BALANCE')        # Use get() to handle possible None values
            }
            print("result is ", customer)
            return  customer
        except Exception as e:
            print(f"Error reading from database: {e}")
            return ["error"]
        finally:
            cur.close()
    # @classmethod
    # def authenticate(cls, mysql, customer_id, password):
    #     account = cls.read(mysql, customer_id)
    #     if account and check_password_hash(account.password, password):
    #         return account  # Authentication successful
    #     return None  # Authentication failed

    @classmethod
    def authenticate(cls, mysql, customer_id):
        account = cls.read(mysql, customer_id)
        if account:
            return account
        else:
            return None
        
    @classmethod
    def create(cls, mysql, password, f_name, l_name, mobile_no, address, initial_balance):
        """Create a new customer in the CUSTOMER table."""
        cursor = mysql.connection.cursor()
        
        # Generate new customer ID (could be auto-generated in a real system)
        cursor.execute("SELECT MAX(CUSTOMER_ID) FROM CUSTOMER")
        result1 = cursor.fetchone()
        new_customer_id = result1[0] + 1 if result1[0] else 1001  # Start from 1001 if no customers exist
        cursor.execute("SELECT MAX(ACCOUNT_NO) FROM ACCOUNT")
        result2 = cursor.fetchone()
        new_account_no = result2[0] + 1 if result2[0] else 3001
        # Insert new customer details
        query1 = """
            INSERT INTO CUSTOMER (CUSTOMER_ID, PASSWORD, F_NAME, L_NAME, MOBILE_NO, ADDRESS)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        query2 = """INSERT INTO ACCOUNT (ACCOUNT_NO, BALANCE, CUSTOMER_ID)
                    VALUES (%s,%s,%s)"""
        cursor.execute(query1, (new_customer_id, password, f_name, l_name, mobile_no, address))
        cursor.execute(query2, (new_account_no, initial_balance, new_customer_id))
        mysql.connection.commit()
        cursor.close()

        return f"Customer {f_name} {l_name} created with ID {new_customer_id}"
    
    @classmethod
    def update(cls, mysql, customer_id, password, f_name, l_name, mobile_no, address):
        cursor = mysql.connection.cursor()
        query = """UPDATE CUSTOMER 
           SET PASSWORD = %s, F_NAME = %s, L_NAME = %s, MOBILE_NO = %s, ADDRESS = %s 
           WHERE CUSTOMER_ID = %s"""

        cursor.execute(query, (password, f_name, l_name, mobile_no, address, customer_id))
        mysql.connection.commit()
        cursor.close()
        return f"Customer {f_name} {l_name} updated with ID {customer_id}"
    
    @classmethod
    def delete(cls, mysql, customer_id):
        cursor = mysql.connection.cursor()
        query1 = """DELETE FROM CUSTOMER WHERE CUSTOMER_ID = %s"""
        cursor.execute(query1, (customer_id,))
        query2 = """DELETE FROM ACCOUNT WHERE CUSTOMER_ID = %s"""
        cursor.execute(query2, (customer_id,))
        mysql.connection.commit()
        cursor.close()
        return f"Customer deleted with ID {customer_id}"

    @classmethod
    def get_loan_details(cls,self, mysql, customer_id):
        """Retrieve loan details for the customer if they exist."""
        if not self.customer_id:
            raise ValueError("Customer ID is required to retrieve loan details.")

        cursor = mysql.connection.cursor()
        query = "SELECT * FROM LOAN WHERE CUSTOMER_ID = %s"
        loan_data = cls._execute_query(mysql, query, (customer_id,))
        loan = cursor.fetchone()
        cursor.close()
        return loan
    
    @classmethod
    def make_loan_payment(self, mysql, payment_amount):
        """Deduct payment from account balance and apply it towards the loan."""
        cursor = mysql.connection.cursor()
        
        # Retrieve account and loan details
        cursor.execute("SELECT ACCOUNT_NO, BALANCE FROM ACCOUNT WHERE CUSTOMER_ID = %s", (self.customer_id,))
        account = cursor.fetchone()
        cursor.execute("SELECT LOAN_NUMBER, AMOUNT FROM LOAN WHERE CUSTOMER_ID = %s", (self.customer_id,))
        loan = cursor.fetchone()

        if not account or not loan:
            cursor.close()
            return "Account or Loan details not found."

        account_no, balance = account
        loan_number, loan_amount = loan

        # Check if there’s enough balance to make the payment
        if balance < payment_amount:
            cursor.close()
            return "Insufficient funds for payment."

        # Deduct from balance and reduce loan amount
        new_balance = balance - payment_amount
        new_loan_amount = loan_amount - payment_amount

        # Update ACCOUNT table
        cursor.execute("UPDATE ACCOUNT SET BALANCE = %s WHERE ACCOUNT_NO = %s", (new_balance, account_no))

        # Update LOAN table
        cursor.execute("UPDATE LOAN SET AMOUNT = %s WHERE LOAN_NUMBER = %s", (new_loan_amount, loan_number))

        # Insert into PAYMENT history
        cursor.execute(
            "INSERT INTO PAYMENT (PAYMENT_DATE, PAYMENT_AMOUNT, LOAN_NUMBER) VALUES (NOW(), %s, %s)",
            (payment_amount, loan_number)
        )

        mysql.connection.commit()
        cursor.close()
        return "Payment successfully processed."
