import os
import csv
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

f = open("books.csv")
reader = csv.reader(f)


# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(os.getenv("DATABASE_URL"))
# DATABASE_URL is an environment variable that indicates where the database lives
db = scoped_session(sessionmaker(bind=engine))

books = db.execute("SELECT * FROM books").fetchall()

for isbn, title, primary_author, year in reader:
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": os.getenv("KEY"), "isbns": isbn})
    print(res)
    if res.status_code == 200:
        data = res.json()
        base = data['books'][0]

        # if not base['average_rating']:
        #     raise Exception(f"error {title} average rating not found")

        # if not base['work_ratings_count']:
        #     raise Exception(f"error {title} work_ratings_count not found")

        i = data['books'][0]['isbn']
        average_score = data['books'][0]['average_rating']
        review_count = data['books'][0]['work_ratings_count']

        db.execute(
            """INSERT INTO books (isbn, title, primary_author, year, review_count, average_score) VALUES (:isbn, :title, :primary_author, :year, :review_count, :average_score)""", {"isbn": isbn, "title": title, "primary_author": primary_author, "year": year, "review_count": review_count, "average_score": average_score})
        print(f"added {title} to books table")
    else:
        pass


db.commit()
