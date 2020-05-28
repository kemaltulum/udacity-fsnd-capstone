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

	return app

APP = create_app()

if __name__ == '__main__':
		APP.run(host='0.0.0.0', port=8080, debug=True)