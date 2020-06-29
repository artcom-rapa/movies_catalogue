from flask import Flask, render_template, request
import tmdb_client
import random

app = Flask(__name__)


@app.route('/')
def homepage():
    selected_list = request.args.get("list_type", "popular")
    lists = ["popular", "top_rated", "upcoming", "now_playing"]
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    random.shuffle(movies)
    return render_template("homepage.html", movies=movies, current_list=selected_list, lists=lists)


@app.errorhandler(404)
def not_found(error):
    movies = tmdb_client.get_movies(how_many=8, list_type="popular")
    return render_template("homepage.html", movies=movies, current_list="popular")


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


if __name__ == '__main__':
    app.run(debug=True)