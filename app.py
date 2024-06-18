from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS parts (
                    id INTEGER PRIMARY KEY,
                    supplier TEXT,
                    part_number TEXT,
                    date TEXT,
                    inspector TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM parts')
    parts = c.fetchall()
    conn.close()
    return render_template('index.html', parts=parts)

@app.route('/add', methods=['POST'])
def add_part():
    supplier = request.form['supplier']
    part_number = request.form['part_number']
    date = request.form['date']
    inspector = request.form['inspector']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO parts (supplier, part_number, date, inspector) VALUES (?, ?, ?, ?)', (supplier, part_number, date, inspector))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:part_id>')
def delete_part(part_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM parts WHERE id = ?', (part_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM parts WHERE supplier LIKE ? OR part_number LIKE ? OR date LIKE ? OR inspector LIKE ?''', 
              ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    parts = c.fetchall()
    conn.close()
    return render_template('index.html', parts=parts)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)