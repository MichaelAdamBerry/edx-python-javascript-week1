def verify(p1, p2):
    return p1 == p2


def msgs(u):
    m = {"u_taken": "That username is already taken. Please try again.",
         "p_match": "Passwords must match. Please try again.",
         "logged_in": f"logged in as {u}",
         "json_e": "404 not found -  double check the isbn number and try again"}
    return m


def format_data(d):
    return {"isbn": d[1], "title": d[2], "author": d[3],
            "year": d[4], "review_count": f"{d[5]}", "average_score": d[6]}


def user_review_exists(u, ls):
    for i, d in enumerate(ls):
        if d['username'] == u:
            return [d, i]
    return False

# returns list of review dicts


def rev_data(book, u):
    r = []
    for bk in book:
        if bk.score is None:
            continue
        else:
            d = {"score": bk['score'], "review_text": bk['review_text'],
                 "book_id": bk['book_id'], "user_id": bk['user_id'], "username": u}
            r.append(d)
    return r

# return book data for book GET req


def bk_data(book):
    d = {'title': book[0]['title'], 'primary_author':
         book[0]['primary_author'], 'isbn': book[0]['isbn'],
         'year': book[0]['year'], 'average_score': book[0]['average_score']}
    return d


# Takes u(string) and r(list of review dicts)
# Returns True or False if user has revieved item in list


def has_r(u, r):
    if len(r) == 0:
        return False
    else:
        for i in r:
            print(i)
            if i[f'username'] == u:
                return True
    return False


def u_r(u, r):
    d = {}
    if len(r) == 0:
        return False
    else:
        for i in r:
            print(i)
            if i[f'username'] == u:
                return i
    return d
