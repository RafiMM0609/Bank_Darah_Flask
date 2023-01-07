import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_content):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE content = ?',
                        (post_content,)).fetchone()
    conn.close()

    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        No_hp = request.form['No_hp']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content,No_hp) VALUES (?, ?, ?)',
                         (title, content, No_hp))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')
@app.route('/search',methods=['GET','POST'])
def posts_lists():
    q = request.args.get('q')
    temp = q
    post = get_post(q)
    if post == None and temp != None:
        flash('Stok Tidak Tersedia')

    return render_template('search.html',post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))