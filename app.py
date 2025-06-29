from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from datetime import date

app = Flask(__name__)

# PostgreSQL connection config
DB_HOST = "localhost"
DB_NAME = "ledgerly"
DB_USER = "postgres"
DB_PASS = "admin"  # <- Replace with your pgAdmin password

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM transactions ORDER BY paid_date DESC')
    expenses = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        category = request.form['category']
        expense_date = request.form['expense_date']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO transactions (description, amount, category, expense_date) VALUES (%s, %s, %s, %s)',
            (description, amount, category, expense_date)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('form.html')

@app.route('/edit/<int:uid>', methods=['GET', 'POST'])
def edit_expense(uid):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        category = request.form['category']
        expense_date = request.form['expense_date']
        cur.execute(
            'UPDATE transactions SET description=%s, amount=%s, category=%s, expense_date=%s WHERE uid=%s',
            (description, amount, category, expense_date, uid)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    cur.execute('SELECT * FROM transactions WHERE uid = %s', (uid,))
    expense = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('form.html', expense=expense)

@app.route('/delete/<int:uid>')
def delete_expense(uid):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM expenses WHERE uid = %s', (uid,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)