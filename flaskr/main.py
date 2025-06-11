from flaskr import app
from flask import render_template , request , redirect , url_for
import sqlite3
DATABASE = 'database.db'

@app.route('/')
def index():
    connection=sqlite3.connect(DATABASE)
    db_books=connection.execute('SELECT * FROM books').fetchall()
    connection.close()

    books=[]
    for row in db_books:
        books.append({
            'title':row[0],
            'author':row[1],
            'arrival_day':row[2],
        })
            
    return render_template(
        'index.html',
        books = books,
    )

@app.route('/search')
def search_results():
    return render_template('search_results.html')

@app.route('/register' , methods=['POST'])
def register():
    title=request.form['title']
    price=request.form['price']
    arrival_day=request.form['arrival_day']

    connection=sqlite3.connect(DATABASE)
    connection.execute('insert into books values (?,?,?)' , [title , price , arrival_day])
    connection.commit()
    connection.close()
    return redirect(url_for('index'))