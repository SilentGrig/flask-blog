# blog.py - controller

# imports
from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
from functools import wraps
import sqlite3
import os

# configuration
DATABASE = "blog.db"
USERNAME = "admin"
PASSWORD = "admin"
SECRET_KEY = "b'z[\xe2\\\xf0\x94\xe7_,\xca\xb2\x92\xc9\x7f4\xdd\xa7\x10W3}R\xc1\xf1'"

app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

# function used for connecting to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    
# check logged in function
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))
    return wrap
    
# App routes
@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == "POST":
        if request.form['username'] != app.config['USERNAME'] or \
            request.form['password'] != app.config['PASSWORD']:
            error = "Invalid Credentials. Please try again."
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template("login.html", error=error), status_code

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    flash("You were logged out")
    return redirect(url_for("login"))
   
@app.route("/main")
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute("SELET * FROM posts")
    posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template("main.html", posts=posts)
    
if __name__ == '__main__':
    app.run(host=os.environ['IP'], port=int(os.environ['PORT']), debug=True)