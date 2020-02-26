from helpers import verify, msgs, format_data, user_review_exists


def test_verify():
    assert verify('abcdefg', 'abcdefg') == True
    assert verify("abcdefg", "adfghjf") == False


def test_msgs():
    all = msgs("me")
    assert all['logged_in'] == "logged in as me"
    assert msgs("me")['logged_in'] == "logged in as me"


def test_format_data():
    d = ["0", "1111", "title", "author", "1986", 200, "1.1"]
    data = format_data(d)
    assert data == {"isbn": "1111", "title": "title", "author": "author",
                    "year": "1986", "review_count": "200", "average_score": "1.1"}


def test_user_review_exists():
    mock_1 = [{"username": "me"}, {"username": "not_me"}]
    mock_2 = [{"username": "me_nope"}, {"username": "not_me"}]
    assert len(mock_2) == 2
    assert user_review_exists("me", mock_1) == [{"username": "me"}, 0]
    assert user_review_exists("me", mock_2) == False
