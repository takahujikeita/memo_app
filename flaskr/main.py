from flaskr import app
from flask import render_template , request , redirect , url_for
import sqlite3

DATABASE = 'database.db'

# db接続
def get_db_connection():
    connection=sqlite3.connect(DATABASE)
    connection.row_factory=sqlite3.Row
    return connection


# カテゴリ分類→ここの拡張性と保守性についてもっとブラッシュアップする必要あり
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


@app.route('/')
def index():

    sql = "SELECT * FROM notes"
    # データベースからデータを取得
    connection=get_db_connection()
    notes=connection.execute(sql).fetchall()
    connection.close()

    return render_template(
        'index.html',
        notes = notes,
    )


@app.route('/register' , methods=['POST'])
def register():
    # フォームからデータを取得
    content=request.form['content']
    category=classify_category(content)

    # dbに保存
    connection=get_db_connection()
    connection.execute(
        'insert into notes (content,category) values (?,?)',
        (content,category)
    )
    connection.commit()
    connection.close()

    return redirect(url_for('index'))

# search関数の中をcontrollerでわけると保守性がます（laravelのディレクトリ分けみたいなやつ）
@app.route('/search')
def search():
    # 検索機能
    # フォームから送られてきた検索条件を取得
    search_category=request.args.get('category' , '')
    search_keyword=request.args.get('keyword' , '').strip()
    search_date=request.args.get('date' , '')

    searched=bool(search_category or search_keyword or search_date)


    sql = "SELECT * FROM notes"
    where_clauses = []
    params = []

# 関数にしてあげたほうがいい
    if search_category:
        where_clauses.append("category = ?")
        params.append(search_category)
    if search_keyword:
        # 大文字・小文字を区別
        where_clauses.append("LOWER(content) LIKE ?")
        params.append(f"%{search_keyword.lower()}%")
    if search_date:
        where_clauses.append("DATE(created_at) = ?")
        params.append(search_date)

# ここも関数にしてあげた方がいい
    # where句が存在する場合、SQL文に追加
    if where_clauses:
        sql +=" where " + " and ".join(where_clauses)

    # 常に新しい順で表示する
    sql+=" order by created_at desc"

    # データベースからデータを取得
    connection=get_db_connection()
    notes=connection.execute(sql,params).fetchall()
    connection.close()

    # 検索条件をテンプレートに渡し
    search_params={
        'category':search_category,
        'keyword':search_keyword,
        'date':search_date,
    }

    return render_template(
        'search.html',
        notes = notes,
        search_params = search_params,
        searched=searched
    )

