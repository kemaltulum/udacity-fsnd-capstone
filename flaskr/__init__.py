import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor

from auth.auth import AuthError, requires_auth

from datetime import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    GET /movies
    Get all movies

    Example Request: curl 'http://localhost:5000/movies'

    Expected Result:
    {
        "movies": [
            {
            "actors": [
                {
                "age": 54,
                "gender": "M",
                "id": 1,
                "movie_id": 2,
                "name": "Tom Hanks"
                },
                {
                "age": 45,
                "gender": "M",
                "id": 4,
                "movie_id": 2,
                "name": "Robert Downey, Jr."
                },
                {
                "age": 45,
                "gender": "F",
                "id": 5,
                "movie_id": 2,
                "name": "Julia Roberts"
                }
            ],
            "id": 2,
            "release_date": "Fri, 04 May 2012 00:00:00 GMT",
            "title": "Yahşi Batı"
            },
            ...
        ],
        "success": true
    }
    '''
    @app.route('/movies', methods=['GET'])
    @requires_auth('view:movies')
    def retrieve_movies(payload):
        movies = Movie.query.all()
        movies = list(map(lambda movie: movie.format(), movies))
        return jsonify({
            "success": True,
            "movies": movies
        })

    '''
    GET /actors
    Get all actors

    Example Request: curl 'http://localhost:5000/actors'

    Expected Result:
    {
        "actors": [
            {
            "age": 45,
            "gender": "M",
            "id": 6,
            "movie_id": 1,
            "name": "Cem Yılmaz"
            },
            {
            "age": 54,
            "gender": "M",
            "id": 1,
            "movie_id": 2,
            "name": "Tom Hanks"
            },
            {
            "age": 44,
            "gender": "M",
            "id": 2,
            "movie_id": 3,
            "name": "Brad Pitt"
            }
        ],
        "success": true
    }
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth('view:actors')
    def retrieve_actors(payload):
        actors = Actor.query.all()
        actors = list(map(lambda actor: actor.format(), actors))
        return jsonify({
            "success": True,
            "actors": actors
        })

    '''
    POST /movies
    Creates a new movie.
    Requires the title and release date.

    Example Request: (Create)
    curl --location --request POST 'http://localhost:5000/movies' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "title": "Pek Yakında",
            "release_date": "2020-02-19"
        }'

    Example Response:
    {
        "success": true
    }
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title is None or release_date is None:
            abort(400, "Missing field for Movie")

        movie = Movie(title=title,
                      release_date=release_date)

        movie.insert()

        return jsonify({
            "success": True
        })

        '''
    POST /actors
    Creates a new actor.
    Requires the name, age and gender of the actor.

    Example Request: (Create)
    curl --location --request POST 'http://localhost:5000/actors' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "name": "Cem Yılmaz",
            "age": "45",
            "gender": "M"
        }'

    Example Response:
    {
        "success": true
    }
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie_id = body.get('movie_id', None)

        if name is None or age is None or gender is None or movie_id is None:
            abort(400, "Missing field for Actor")

        actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)

        actor.insert()

        return jsonify({
            "success": True
        })

    '''
    DELETE /movies/<int:movie_id>
    Deletes the movie with given id

    Example Request: curl --request DELETE 'http://localhost:5000/movies/1'

    Example Response:
    {
        "deleted": 1,
        "success": true
    }
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404, "No movie with given id " + str(movie_id) + " is found")

        movie.delete()

        return jsonify({
            'success': True,
            'deleted': movie_id
        })

    '''
    DELETE /actors/<int:actor_id>
    Deletes the actor with given id

    Example Request: curl --request DELETE 'http://localhost:5000/actors/1'

    Example Response:
    {
        "deleted": 1,
        "success": true
    }
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404, "No actor with given id " + str(actor_id) + " is found")

        actor.delete()

        return jsonify({
            'success': True,
            'deleted': actor_id
        })

    '''
    PATCH /movies/<movie_id>
        Updates the movie where <movie_id> is the existing movie id
        Responds with a 404 error if <movie_id> is not found
        Update the corresponding fields for Movie with id <movie_id>

    Example Request:
    curl --location --request PATCH 'http://localhost:5000/movies/1' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "title": "Eyvah eyvah 2"
        }'

    Example Response:
    {
        "success": true,
        "updated": {
            "id": 1,
            "release_date": "Wed, 04 May 2016 00:00:00 GMT",
            "title": "Eyvah eyvah 2"
        }
    }
    '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie(payload, movie_id):

        updated_movie = Movie.query.get(movie_id)

        if not updated_movie:
            abort(
                404,
                'Movie with id: ' +
                str(movie_id) +
                ' could not be found.')

        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title:
            updated_movie.title = title
        if release_date:
            updated_movie.release_date = release_date

        updated_movie.update()

        return jsonify({
            "success": True,
            "updated": updated_movie.format()
        })

    '''
    PATCH /actors/<actor_id>
        Updates the actor where <actor_id> is the existing actor id
        Responds with a 404 error if <actor_id> is not found
        Update the given fields for Actor with id <actor_id>

    Example Request:
    curl --location --request PATCH 'http://localhost:5000/actors/1' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "name": "Tom Hanks"
        }'

    Example Response:
    {
        "success": true,
        "updated": {
            "age": 54,
            "gender": "M",
            "id": 1,
            "name": "Tom Hanks"
        }
    }
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actor(payload, actor_id):

        updated_actor = Actor.query.get(actor_id)

        if not updated_actor:
            abort(
                404,
                'Actor with id: ' +
                str(actor_id) +
                ' could not be found.')

        body = request.get_json()

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie_id = body.get('movie_id', None)

        if name:
            updated_actor.name = name
        if age:
            updated_actor.age = age
        if gender:
            updated_actor.gender = gender
        if movie_id:
            updated_actor.movie_id = movie_id

        try:
            updated_actor.update()
        except BaseException:
            abort(
                400,
                "Bad formatted request due to nonexistent movie id" +
                str(movie_id))

        return jsonify({
            "success": True,
            "updated": updated_actor.format()
        })

    def get_error_message(error, default_message):
        try:
            return error.description
        except BaseException:
            return default_message

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": get_error_message(error, "unprocessable"),
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": get_error_message(error, "resource not found")
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": get_error_message(error, "bad request")
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(auth_error):
        return jsonify({
            "success": False,
            "error": auth_error.status_code,
            "message": auth_error.error['description']
        }), auth_error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
