"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

movies_in_db = []
for movie in movie_data:
    # TODO: get the title, overview, and poster_path from the movie
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime
    title =movie["title"]
    overview =movie["overview"]
    poster_path = movie["poster_path"]
    
    date_str = movie["release_date"]
    format = "%Y-%m-%d"
    date = datetime.strptime(date_str, format)

    new_movie = crud.create_movie(title, overview, date, poster_path)
    movies_in_db.append(new_movie)
    
model.db.session.add_all(movies_in_db)
model.db.session.commit()
    
for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    # TODO: create a user here
    new_user = crud.create_user(email, password)
    model.db.session.add(new_user)

    # TODO: create 10 ratings for the user
    for n in range(10):
    
        rand_movie = choice(movies_in_db)
        score = randint(1, 5)

        new_rating = crud.create_rating(new_user, rand_movie, score)
        model.db.session.add(new_rating)

model.db.session.commit()