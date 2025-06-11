from flaskr import app
from flask import render_template , request , redirect , url_for
import sqlite3
DATABASE = 'database.db'

@app.route('/')
def index():
    connection=sqlite3.connect(DATABASE)
    db_notes=connection.execute('SELECT * FROM notes').fetchall()
    connection.close()

    notes=[]
    for row in db_notes:
        notes.append({
            'id':row[0],
            'created_at':row[1],
            'content':row[2],
            'category':row[3]
        })
            
    return render_template(
        'index.html',
        notes = notes,
    )

# カテゴリ分類
def classify_category(content):
    # メモの内容からカテゴリを自動で分類する
    # switch文にする
    if '会議' in content or '打ち合わせ' in content:
        return 'Meeting'
    elif '買い物' in content or '購入' in content:
        return 'Shopping'
    elif 'TODO' in content or 'やること' in content:
        return 'Task'
    else:
        return 'Other'


@app.route('/register' , methods=['POST'])
def register():
    # フォームからデータを取得
    content=request.form['content']
    category=classify_category(content)

    connection=sqlite3.connect(DATABASE)
    connection.execute('insert into notes (content , category) values (?,?)' , [content , category])
    connection.commit()
    connection.close()
    return redirect(url_for('index'))