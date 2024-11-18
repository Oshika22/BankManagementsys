function showForm(type) {
    // // Hide both forms initially
    // document.getElementById('employeeForm').style.display = 'none';
    // document.getElementById('customerForm').style.display = 'none';

    // Show the selected form
    if (type === 'employee') {
        window.location.href = '/employee_login';
    } else if (type === 'customer') {
        window.location.href = '/customer_login';
    }
}