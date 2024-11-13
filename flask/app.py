from flask import Flask, render_template, jsonify 
from flask_mysqldb import MySQL
from config import Config
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(Config)
mysql = MySQL(app)
@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/view_bank/<int:code>')
def view_bank(code):
    bank = Bank.read(code)
    return render_template('view_bank.html', bank=bank)


if __name__ == "__main__":
    app.run(debug=True,port=8000)