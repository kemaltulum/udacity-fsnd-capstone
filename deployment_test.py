import os
import unittest
import json

import requests


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.api = "https://casting-agency-fsnd-kml.herokuapp.com"

        self.movie = {
            "title": "Pek Yakında",
            "release_date": "19-02-2020"
        }

        self.actor = {
            "name": "Cem Yılmaz",
            "age": 45,
            "gender": 'M',
            "movie_id": 2
        }

        # Set up authentication tokens info
        with open('auth_config.json', 'r') as f:
            self.auth = json.loads(f.read())

        assistant_jwt = self.auth["roles"]["Casting Assistant"]["jwt_token"]
        director_jwt = self.auth["roles"]["Casting Director"]["jwt_token"]
        producer_jwt = self.auth["roles"]["Executive Producer"]["jwt_token"]
        self.auth_headers = {
            "Casting Assistant": f'Bearer {assistant_jwt}',
            "Casting Director": f'Bearer {director_jwt}',
            "Executive Producer": f'Bearer {producer_jwt}'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = requests.get(self.api + '/movies', headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["movies"]), type([]))

    def test_get_actors(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = requests.get(self.api + '/actors', headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["actors"]), type([]))

    def test_get_actors_by_director(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        res = requests.get(self.api + '/actors', headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["actors"]), type([]))

    def test_get_actor_fail_401(self):
        res = requests.get(self.api + '/actors')
        data = res.json()

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(type(data["message"]), type(""))

    def test_create_movies_fail_400(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        movie_fail = {"title": "Movie"}
        res = requests.post(
            self.api + f'/movies',
            json=movie_fail,
            headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Missing field for Movie")

    def test_create_movies_fail_403(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        movie_fail = {"title": "Movie"}
        res = requests.post(
            self.api + f'/movies',
            json=movie_fail,
            headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_create_actors_fail_400(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        actor_fail = {"name": "Actor"}
        res = requests.post(
            self.api + f'/actors',
            json=actor_fail,
            headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Missing field for Actor")

    def test_create_actors_fail_403(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        actor_fail = {"name": "Actor"}
        res = requests.post(
            self.api + f'/actors',
            json=actor_fail,
            headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
