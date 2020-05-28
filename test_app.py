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
		self.assertEqual(len(data["movies"]), 4)

	def test_get_actors(self):
		res = self.client().get('/actors')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])
		self.assertEqual(type(data["actors"]), type([]))
		self.assertEqual(len(data["actors"]), 5)

	def test_create_movies(self):
		res = self.client().post(f'/movies', json=self.movie)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])

		res_2 = self.client().get('/movies')
		data_2 = json.loads(res_2.data)

		self.assertEqual(len(data_2["movies"]), 5)

		self.delete_id_movie = data_2[-1]["id"]

	def test_create_movies_fail_400(self):
		res = self.client().post(f'/movies', json={"title": "name"})
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 400)
		self.assertFalse(data['success'])
		self.assertEqual(data['message'], "Missing field for Movie")

	def test_create_actors(self):
		res = self.client().post(f'/actors', json=self.actor)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])

		res_2 = self.client().get('/actors')
		data_2 = json.loads(res_2.data)

		self.assertEqual(len(data_2["actors"]), 6)

		self.delete_id_actor = data_2[-1]["id"]

	def test_create_actors_fail_400(self):
		res = self.client().post(f'/actors', json={"name": "name"})
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 400)
		self.assertFalse(data['success'])
		self.assertEqual(data['message'], "Missing field for Actor")

	def test_delete_movie(self):
		res = self.client().delete(f'/movies/{self.delete_id_movie}')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])

		res = self.client().get('/movies')
		m_data = json.loads(res.data)

		found_deleted = False

		for m in m_data["movies"]:
			if m["id"] == self.delete_id_movie:
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
		res = self.client().delete(f'/actors/{self.delete_id_actor}')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])

		res = self.client().get('/actors')
		a_data = json.loads(res.data)

		found_deleted = False

		for a in a_data["actors"]:
			if a["id"] == self.delete_id_actor:
				found_deleted = True
				break
	
		self.assertFalse(found_deleted)

	def test_delete_actor_fail_404(self):
		a_id = -100
		res = self.client().delete(f'/actors/{a_id}')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 404)
		self.assertFalse(data['success'])

	

# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()