import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__)
	setup_db(app)

	CORS(app)

	# CORS Headers 
	@app.after_request
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
		response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
		return response

	'''
	GET /movies 
	Get all movies

	Example Request: curl 'http://localhost:5000/movies'

	Expected Result:
	{
		"movies": [
			{
				"id": 1, 
				"release_date": "Wed, 04 May 2016 00:00:00 GMT", 
				"title": "Captain America: Civil War"
			}, 
			{
				"id": 2, 
				"release_date": "Fri, 04 May 2012 00:00:00 GMT", 
				"title": "Yah\u015fi Bat\u0131"
			}, 
			{
				"id": 3, 
				"release_date": "Fri, 14 May 2010 00:00:00 GMT", 
				"title": "The Avengers"
			}, 
			{
				"id": 4, 
				"release_date": "Wed, 11 Sep 2019 00:00:00 GMT", 
				"title": "The Martian"
			}
		], 
		"success": true
	}
	'''
	@app.route('/movies', methods=['GET'])
	def retrieve_movies():
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
				"age": 54, 
				"gender": "M", 
				"id": 1, 
				"name": "Tom Hanks"
			}, 
			{
				"age": 44, 
				"gender": "M", 
				"id": 2, 
				"name": "Brad Pitt"
			}, 
			{
				"age": 35, 
				"gender": "F", 
				"id": 3, 
				"name": "Scarlett Johansson"
			}, 
			{
				"age": 45, 
				"gender": "M", 
				"id": 4, 
				"name": "Robert Downey, Jr."
			}, 
			{
				"age": 45, 
				"gender": "F", 
				"id": 5, 
				"name": "Julia Roberts"
			}
		], 
		"success": true
	}
	'''
	@app.route('/actors', methods=['GET'])
	def retrieve_actors():
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
			"release_date": "19-02-2020"
		}'

	Example Response: 
	{
		"success": true
	}
	'''
	@app.route('/movies', methods=['POST'])
	def create_movie():
		body = request.get_json()

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
	def create_actor():
		body = request.get_json()

		name = body.get('name', None)
		age = body.get('age', None)
		gender = body.get('gender', None)


		if name is None or age is None or gender is None:
			abort(400, "Missing field for Actor")
		
		actor = Actor(name=name, age=age, gender=gender)

		actor.insert()

		return jsonify({
			"success": True
		})

		
	def get_error_message(error, default_message):
		try:
			return error.description
		except:
			return default_message

	## Error Handling

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

	"""
	@app.errorhandler(AuthError)
	def auth_error(auth_error):
		return jsonify({
			"success": False, 
			"error": auth_error.status_code,
			"message": auth_error.error['description']
			}), auth_error.status_code
	"""

	return app

APP = create_app()

if __name__ == '__main__':
		APP.run(host='0.0.0.0', port=8080, debug=True)