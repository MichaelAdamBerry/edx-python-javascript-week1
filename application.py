import os

from flask import Flask, session, redirect, flash, url_for, request, render_template, jsonify, make_response
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from markupsafe import escape, soft_unicode
from werkzeug.security import generate_password_hash, check_password_hash
import helpers
import queries

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# # Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# # app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        if request.method == 'POST':
            t = request.form['search_type']
            v = escape(request.form['search'])
            return redirect(f'/search/{v}/{t}')
        return render_template("search.html", username=session['username'])
    return render_template("landing.html")


@app.route('/search/<str>/<t>', methods=['GET'])
def search(str, t):
    s = escape(str)
    print(f"escaped str {s}")
    print(f"search type is {t}")
    q = f"SELECT * FROM books WHERE {t} LIKE '%{s}%'"
    c = db.execute(q).rowcount
    if c == 0:
        flash('No search results found')
        return redirect(f"/")
    list_items = db.execute(q).fetchall()
    print(f"results {list_items}")
    return render_template('list.html', list_items=list_items, str=str, t=t)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = escape(request.form['username'])
        rowcount = db.execute(
            f"SELECT * FROM users WHERE username = '{u}';").rowcount

        # if user does not exist return to login
        if rowcount == 0:
            flash("Username does not exist. Please try again")
            return render_template("login.html")

        user_data = db.execute(
            f"SELECT * FROM users WHERE username = '{u}';").fetchone()

        # if hashed password in db does not match password input
        # return to login
        if check_password_hash(
                user_data['password'], request.form['password']) == False:
            flash("check the password and try again")
            return render_template("login.html")

        # save username to session and redirect to search view
        session['username'] = u
        db.execute(
            f"UPDATE users SET logged_in = TRUE WHERE users.username = '{u}'")
        db.commit()
        return redirect(url_for('index', name=session['username']))
    # for GET requests end current session and render login form
    if not session.get('username') is None:
        u = session['username']
        db.execute(
            f"UPDATE users SET logged_in = FALSE WHERE users.username = '{u}'")
        db.commit()
    session.pop('username', None)
    return render_template("login.html")


@app.route('/logout')
def logout():
    u = session['username']
    q = queries.logout(u)
    # update logged_in boolean in user table where username
    db.execute(q[0], q[1])
    db.commit()
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = escape(request.form['username'])
        p = escape(request.form['password'])
        rp = escape(request.form['re_enter'])

        q = queries.find(u)
        p_match = helpers.verify(p, rp)
        hashed_p = generate_password_hash(p, "sha256")
        found = db.execute(q).fetchone()
        if found != None:
            flash(helpers.msgs(u)['logged_in'])
            return redirect(url_for("register"))
        if p_match == False:
            flash(helpers.msgs(u)['p_match'])
            return redirect(url_for("register"))
        # set session data to logged in
        session['username'] = u
        q = queries.register(u, hashed_p, p_match)
        db.execute(q[0], q[1])
        db.commit()
        flash(helpers.msgs(u)['logged_in'])
        return redirect(url_for("index"))
    else:
        return render_template("register.html")


@app.route('/book/<isbn>', methods=['GET', 'POST'])
def book(isbn):
    # POST request made to removes existing review
    u = session['username']
    if request.method == 'POST':
        db.execute(queries.del_rev(u, isbn))
        db.commit()
        print(f"removing review - isbn {isbn} by {u} from database")
        return redirect(f'/book/{isbn}')

    # reviews = db.execute(queries.get_book(u, isbn)).fetchall()
    book = db.execute(f"SELECT * FROM books WHERE isbn = '{isbn}';"
                      ).fetchall()
    reviews = db.execute(
        f"SELECT * FROM reviews WHERE book_isbn = '{isbn}'").fetchall()

    is_u_r = False

    if not reviews:
        r_empty = True
        print("the list is empty")
    else:
        r_empty = False
        for d in reviews:
            if d['username'] == session['username']:
                is_u_r = True
    print(f" is_u_r ? {is_u_r}")

    data = {
        "is_u_r": is_u_r,
        "u": session['username'],
        "r": reviews,
        "r_empty": r_empty,
        "b": helpers.bk_data(book),
    }

    return render_template("book.html", data=data)


@app.route('/add_review/<isbn>', methods=['POST', 'GET'])
def review(isbn):
    if request.method == 'POST':
        u = session['username']
        v = request.form['stars']
        rt = escape(request.form['review_text'])
        db.execute(queries.add_rev(v, rt, isbn, u))
        db.commit()
        print(
            f"adding review - isbn {isbn} by {u} to database")
        return redirect(f"/book/{isbn}")
    return render_template("add_review.html")


@app.route('/api/<isbn>')
def api(isbn):
    try:
        data = db.execute(queries.get_book_data(isbn)).fetchall()
        headers = {"Content-Type": "application/json"}
        return make_response(jsonify(helpers.format_data(data[0]), 200, headers))
    except:
        return make_response(helpers.msgs("any")['json_e'], 404, headers)
