import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Movie, Actor

class CapstoneTestCase(unittest.TestCase):

	def setUp(self):
		self.app = create_app()
		self.client = self.app.test_client
		self.database_name = "capstone_test"
		self.database_path = "postgres:///{}".format(self.database_name)
		setup_db(self.app, self.database_path)

		# binds the app to the current context
		with self.app.app_context():
			self.db = SQLAlchemy()
			self.db.init_app(self.app)
			# create all tables
			self.db.create_all()

		self.movie = {
			"title": "Pek Yakında",
			"release_date": "19-02-2020"
		}

		self.actor = {
			"name": "Cem Yılmaz",
			"age": 45,
			"gender": 'M'
		}
	
	def tearDown(self):
		"""Executed after reach test"""
		pass

	def test_get_movies(self):
		res = self.client().get('/movies')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])
		self.assertEqual(type(data["movies"]), type([]))

	def test_get_actors(self):
		res = self.client().get('/actors')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])
		self.assertEqual(type(data["actors"]), type([]))

	def test_create_movies(self):
		res = self.client().post(f'/movies', json=self.movie)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])

	def test_create_movies_fail_400(self):
		movie_fail = {"title": "Movie"}
		res = self.client().post(f'/movies', json=movie_fail)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 400)
		self.assertFalse(data['success'])
		self.assertEqual(data['message'], "Missing field for Movie")

	def test_create_actors(self):
		res = self.client().post(f'/actors', json=self.actor)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])

	def test_create_actors_fail_400(self):
		actor_fail = {"name": "Actor"}
		res = self.client().post(f'/actors', json=actor_fail)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 400)
		self.assertFalse(data['success'])
		self.assertEqual(data['message'], "Missing field for Actor")

	def test_delete_movie(self):
		delete_id_movie = 1
		res = self.client().delete(f'/movies/{delete_id_movie}')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])
		self.assertEqual(data['deleted'], delete_id_movie)

		res = self.client().get('/movies')
		m_data = json.loads(res.data)

		found_deleted = False

		for m in m_data["movies"]:
			if m["id"] == delete_id_movie:
				found_deleted = True
				break
	
		self.assertFalse(found_deleted)

	def test_delete_movie_fail_404(self):
		m_id = -100
		res = self.client().delete(f'/questions/{m_id}')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 404)
		self.assertFalse(data['success'])

	def test_delete_actor(self):
		delete_id_actor = 1
		res = self.client().delete(f'/actors/{delete_id_actor}')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])
		self.assertEqual(data['deleted'], delete_id_actor)

		res = self.client().get('/actors')
		a_data = json.loads(res.data)

		found_deleted = False

		for a in a_data["actors"]:
			if a["id"] == delete_id_actor:
				found_deleted = True
				break
	
		self.assertFalse(found_deleted)

	def test_delete_actor_fail_404(self):
		a_id = -100
		res = self.client().delete(f'/actors/{a_id}')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 404)
		self.assertFalse(data['success'])

	def test_update_movie(self):
		update_id_movie = 2
		new_title = "Eyvah eyvah 2"
		res = self.client().patch(f'/movies/{update_id_movie}', json={'title': new_title})
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])
		self.assertEqual(data['updated']['id'], update_id_movie)
		self.assertEqual(data['updated']['title'], new_title)

	def test_update_movie_fail_404(self):
		update_id_movie = -100
		res = self.client().patch(f'/movies/{update_id_movie}')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 404)
		self.assertFalse(data['success'])

	def test_update_actor(self):
		update_id_actor = 2
		new_name = "Tom Hanks"
		new_age = 54
		res = self.client().patch(f'/actors/{update_id_actor}', json={'name': new_name, 'age': new_age})
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])
		self.assertEqual(data['updated']['id'], update_id_actor)
		self.assertEqual(data['updated']['name'], new_name)
		self.assertEqual(data['updated']['age'], new_age)

	def test_update_actor_fail_404(self):
		update_id_actor = -100
		res = self.client().patch(f'/actors/{update_id_actor}')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 404)
		self.assertFalse(data['success'])

	

# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()