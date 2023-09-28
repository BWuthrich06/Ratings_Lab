"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined




app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route("/")
def homepage():
    """View Homepage"""
    
    return render_template("homepage.html")


@app.route("/movies")
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies = movies)


@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""
    
    movie = crud.get_movie_by_id(movie_id)

    
    return render_template("movie_details.html", movie = movie)

@app.route("/movies/<movie_id>/ratings", methods = ['POST'])
def new_rating(movie_id):
    logged_in = session.get("email")


    if logged_in is None:
        flash("you have to login first")
    else:
        rating_score = request.form.get("rating")
        user = crud.get_user_by_email(logged_in)
        movie = crud.get_movie_by_id(movie_id)
        rating = crud.create_rating(user, movie, int(rating_score))
        db.session.add(rating)
        db.session.commit()

    return redirect ("/movies/<movie_id>/")



@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users = users)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new users."""

    email = request.form.get("email")
    password = request.form.get("password")

    if crud.get_user_by_email(email):

        flash("Can't use that email to create account! Try again ya dingus")
    
    else:    

        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully, you can now login.")
        
    return redirect("/")


@app.route("/login", methods =["POST"])
def process_login():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    
    if not user or user.password != password:
        flash("email or password incorrect.")
    else:
        flash("Login complete!")
        session['email'] = email
        
    return redirect("/")


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""
    
    user = crud.get_user_by_id(user_id)
    
    return render_template("user_details.html", user = user)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
