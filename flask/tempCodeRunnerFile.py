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