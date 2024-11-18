from flask import current_app
from werkzeug.security import check_password_hash
import MySQLdb.cursors

class Employee:
    def __init__(self, emp_id=None, emp_name=None, mobile_no=None, address=None):
        self.emp_id = emp_id
        self.emp_name = emp_name
        self.mobile_no = mobile_no
        self.address = address
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
    def read(cls, mysql, emp_id):
        query = "SELECT * FROM EMPLOYEE WHERE EMP_ID = %s"
        employee_data = cls._execute_query(mysql, query, (emp_id,))
        if employee_data:
            return cls(
                emp_id=employee_data['EMP_ID'],
                emp_name=employee_data['EMP_NAME'],
                mobile_no=employee_data['MOBILE_NO'],
                address=employee_data['ADDRESS'],
            )
        return None

    @classmethod
    def authenticate(cls, mysql, emp_id):
        return cls.read(mysql, emp_id)