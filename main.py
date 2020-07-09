import datetime
from flask import Flask, render_template, url_for, request, redirect, flash
import tmdb_client
import random

app = Flask(__name__)

FAVORITES = set()

app.secret_key = b'bulb'


@app.route('/')
def homepage():
    selected_list = request.args.get("list_type", "popular")
    lists = ["popular", "top_rated", "upcoming", "now_playing"]
    if selected_list not in lists:
        selected_list = "popular"
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    random.shuffle(movies)
    return render_template("homepage.html", movies=movies, current_list=selected_list, lists=lists)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.context_processor
def utility_processor():
    def tmdb_movie_info(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_movie_info": tmdb_movie_info}


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id, how_many=4)
    backdrops = tmdb_client.get_single_movie_images(movie_id)
    random.shuffle(backdrops['backdrops'])
    return render_template("movie_details.html", movie=details, cast=cast, backdrops=backdrops)


@app.route('/search')
def search():
    search_query = request.args.get("q", "")
    if search_query:
        movies = tmdb_client.search(search_query=search_query)
    else:
        movies = []
    return render_template("search.html", movies=movies, search_query=search_query)


@app.route('/today')
def today():
    movies = tmdb_client.get_airing_today()
    today = datetime.date.today()
    return render_template("today.html", movies=movies, today=today)


@app.route("/favorites")
def show_favorites():
    if FAVORITES:
        movies = []
        for movie_id in FAVORITES:
            movie_details = tmdb_client.get_single_movie(movie_id)
            movies.append(movie_details)
    else:
        movies = []
    return render_template("homepage.html", movies=movies)


@app.route("/favorites/add", methods=['POST'])
def add_to_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        FAVORITES.add(movie_id)
        flash(f'Dodano film {movie_title} do ulubionych!')
    return redirect(url_for('homepage'))


if __name__ == '__main__':
    app.run(debug=True)