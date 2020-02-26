from queries import logout, find, register, del_rev, get_book, add_rev, get_book_data


def test_logout():
    q = logout('me')
    assert q[0] == "UPDATE users SET logged_in = FALSE WHERE username = :username"
    assert q[1] == {"username": 'me'}


def test_find():
    q = find("me")
    assert q == f"SELECT password FROM users WHERE username = 'me'"


def test_register():
    q = register("me", "password", True)
    assert q[0] == 'INSERT INTO users (username, password, logged_in) VALUES (:username, :password, :logged_in)'
    assert q[1] == {"username": "me",
                    "password": "password", "logged_in": True}


def test_del_rev():
    assert del_rev("me", "1111") == f"DELETE FROM reviews USING users, books  WHERE (SELECT id FROM users WHERE users.username = 'me') = reviews.user_id AND (SELECT id FROM books WHERE books.isbn = '1111') = reviews.book_id;"


def test_get_book():
    assert get_book(
        "me", "1111") == f"SELECT * FROM books LEFT JOIN (reviews JOIN users ON users.id = reviews.user_id) ON reviews.book_id = books.id WHERE books.isbn = '1111'"


def test_get_book_data():
    assert get_book_data("1111") == f"SELECT * FROM books WHERE isbn = '1111'"
