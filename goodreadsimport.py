import csv
import os
import requests
import urllib3
import xmltodict

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://ogunfriattpack:6084243ceb1f939e574a96f953366c04e509075f182edd0089fdef631acd65a5@ec2-18-235-97-230.compute-1.amazonaws.com:5432/d2gkkmcmdcahl4")
db = scoped_session(sessionmaker(bind=engine))

def extract():
    isbntable = db.execute("SELECT isbn FROM books").fetchall()
    # print(isbntable)
    # j = 1
    url = "https://www.goodreads.com/book/review_counts.json?key={uaE76ht3BP8fSW3tl6RoQ}&isbns="
    for i in range(len(isbntable)):
        # if i == 5002:
        #     break
        if i > 4000:
            u = requests.get(url+isbntable[i][0]) 
            print(i, u)
            if u.status_code == 200:
                x = u.json()
                # print(x)
                count = x['books'][0]['ratings_count']
                avgRating = float(x['books'][0]['average_rating'])
                # avgRating = int(avgRating)
                db.execute("INSERT INTO goodreviews (isbn, reviewcount, avgratings) VALUES (:isbn, :reviewcount, :avgratings)", {"isbn":isbntable[i][0], "reviewcount":count, "avgratings":avgRating})
                print(isbntable[i][0], count, avgRating, "succesfully added", i)
        # j += 1
    db.commit()
# if __name__=="__main__":
#     main()

extract()