import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://ogunfriattpack:6084243ceb1f939e574a96f953366c04e509075f182edd0089fdef631acd65a5@ec2-18-235-97-230.compute-1.amazonaws.com:5432/d2gkkmcmdcahl4")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    i = 0
    for isbn, title, author, year in reader:
        print(year,type(year))
        if i > 0:
            year = int(year)
            # print(type(year))
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn":isbn, "title":title, "author":author, "year":year})
            print("added", isbn, title, author, year)
        i += 1
    db.commit()

if __name__=="__main__":
    main()