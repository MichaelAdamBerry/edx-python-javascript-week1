def logout(u):
    q = ["UPDATE users SET logged_in = FALSE WHERE username = :username", {
        "username": u}]
    return q


def find(u):
    return f"SELECT password FROM users WHERE username = '{u}'"


def register(u, p, l):
    return ["INSERT INTO users (username, password, logged_in) VALUES (:username, :password, :logged_in)", {"username": u, "password": p, "logged_in": l}]


def del_rev(u, isbn):
    return f"DELETE FROM reviews USING users, books  WHERE (SELECT id FROM users WHERE users.username = '{u}') = reviews.user_id AND (SELECT id FROM books WHERE books.isbn = '{isbn}') = reviews.book_id;"


def add_rev(v, rt, isbn, u):
    return f"INSERT INTO reviews (score, review_text, book_isbn, username, user_id, book_id) SELECT {v}, '{rt}', '{isbn}', '{u}', u.id, b.id FROM users u, books b WHERE u.username = '{u}' AND b.isbn = '{isbn}';"


def get_book(u, isbn):
    return f"SELECT * FROM books LEFT JOIN (reviews JOIN users ON users.id = reviews.user_id) ON reviews.book_id = books.id WHERE books.isbn = '{isbn}'"

# reviews by book id not isbn


def get_book_all(u, isbn):
    return f"SELECT * FROM books LEFT JOIN (reviews JOIN users ON users.id = reviews.user_id) ON reviews.book_id = books.id WHERE books.isbn = '{isbn}'"


def get_book_data(isbn):
    return f"SELECT * FROM books WHERE isbn = '{isbn}'"
