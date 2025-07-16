from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database table
def init_db():
    conn = sqlite3.connect('rsvp.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            coming TEXT NOT NULL,
            number_of_people INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def rsvp_form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    coming = request.form['coming']
    number = int(request.form['number'])

    conn = sqlite3.connect('rsvp.db')
    c = conn.cursor()
    c.execute("INSERT INTO guests (name, coming, number_of_people) VALUES (?, ?, ?)", (name, coming, number))
    conn.commit()
    conn.close()

    return render_template('thankyou.html')

@app.route('/summary')
def summary():
    conn = sqlite3.connect('rsvp.db')
    c = conn.cursor()
    c.execute("SELECT * FROM guests WHERE coming = 'yes'")
    guests = c.fetchall()
    total_people = sum([g[3] for g in guests])
    conn.close()
    return render_template('summary.html', guests=guests, total=total_people)


@app.route('/admin/summary')
def admin_summary():
    conn = sqlite3.connect('rsvp.db')
    c = conn.cursor()
    c.execute("SELECT name, number_of_people FROM guests WHERE coming = 'yes'")
    guests = c.fetchall()
    total = sum([g[1] for g in guests])
    conn.close()

    return render_template('summary.html', guests=guests, total=total)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
