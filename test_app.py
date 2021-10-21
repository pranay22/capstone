import os
import re
import unittest
import json
from unittest import result
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies

# Tests

class CastingAgencyTest(unittest.TestCase):

    def setUp(self):

        DATABASE_URL = 'postgres://postgres:12345678@localhost:5432/castagency'
        ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFHbVNvLXplMEtHRFE1NUlid3BqMCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zbmNkcjZlby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MDE3YWQ0MmNmYmUwMDY5MGQ3MGEzIiwiYXVkIjoiY2FzdGluZ0FnZW5jeSIsImlhdCI6MTYzNDg0NTc4MCwiZXhwIjoxNjM0ODUyOTgwLCJhenAiOiJyRWdDRGtYWTNXN2ZmWTgyN2Y5R2hzdGUxWHlnSjUzeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycy1kZXRhaWwiLCJnZXQ6bW92aWVzLWRldGFpbCJdfQ.tGpjFHDhp_-3dsgYb1ZHewddifBDdpDzZUkW_ejHzVaD8MKyiVAw08JUQCxYQadHRxyqS6eUfSExBZkj3FE0laic1lVPk77pF6E_qL_OqMcjChqPc-h-Puhz62n3NoIprfsr22tdNwD4_mhcZh9JQVa2G8tNHB1Udu5gNgql0jSm7K8Xbx1Etjf0MQrDuOmoOul-rY1M-8sRYvlHxc58hCeXyAZeAn_3A5_EJ08lz6vR8VEQX20QkAUdEIfy9e8WYgCjSFOHyks1E8_zF2n0AoDTUVo9wgZxFkAyRK5lxAQvKb9R2tHJwOWXl0_k0VK7-ubVLKq4XA6bVo5mX4o7PA'
        PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFHbVNvLXplMEtHRFE1NUlid3BqMCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zbmNkcjZlby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MDE3ZWQxYzI3ODkwMDY4MzFjMjM4IiwiYXVkIjoiY2FzdGluZ0FnZW5jeSIsImlhdCI6MTYzNDg0NTk4NCwiZXhwIjoxNjM0ODUzMTg0LCJhenAiOiJyRWdDRGtYWTNXN2ZmWTgyN2Y5R2hzdGUxWHlnSjUzeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0Om1vdmllcy1kZXRhaWwiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.uC7yNQBcBMVodKm3HRelhEeWQEJ9R6-ujK36Cx6MFwjEuOsu52WNvxdsiWxcdXtmMfaj4ZjSYJpvAvF8Mu6oTNFUi0bFo5MqZV6WoX1x541g1RI64Dwvh4NVrLUmU2DctatU7yU0MZaJVvP90J1SnH8Q44LkNg6jBMgEZI8-aHVU2OMAcOcBxpS6NkBUruBffbohJQBnUQNe9esGTJhj7Y3j7E6cF_7mGWppeJ6MqshEe2Yz4Lu1G4WtfzjsG5dyqSNz7XknreMCz1BCzJRIKlcXNxtfzFisVttYOE4ctO5JX9hzN77QX8ePeGQGNJOeve_xMYmkjfIPCWjAVKO8hg'
        DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFHbVNvLXplMEtHRFE1NUlid3BqMCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zbmNkcjZlby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MDE4M2M1Y2Q5NmIwMDcwMzI4NWMzIiwiYXVkIjoiY2FzdGluZ0FnZW5jeSIsImlhdCI6MTYzNDg0NjA2NCwiZXhwIjoxNjM0ODUzMjY0LCJhenAiOiJyRWdDRGtYWTNXN2ZmWTgyN2Y5R2hzdGUxWHlnSjUzeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzLWRldGFpbCIsImdldDptb3ZpZXMtZGV0YWlsIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.HxU4MoYOYLncj7wZqYcs1inRbYhV-yvzrAFpywPShBTm5ub1firfg9edPRoshTr69tdtJlXl9T3DA4jKyEUlruW4-ZpmN-SzesEzckceOepRchI2-jvXIGOhbI0pYX3XfHsNlcWQ1bh2vMO6NYl17T6wChrEDsvJMjdHskCp4-i4aNGPMldg4Sc9M2PGbG2k3mMTIcqFV26HAbGKRwlYfktQNvap5GQVfvS1aodpLf6IDWs17WNZ-VPmgmNOsGJzwuMy3Xr5GCBwy-bPu1cNpYLZeA9oJ6pPtDuXouvz48owILW44PQThTl2Fo4kxmkTVtQ-4grEQrJdEZp0SsQl-A'

        self.assistant_auth_header = {'Authorization':
                                      'Bearer ' + ASSISTANT_TOKEN}
        self.producer_auth_header = {'Authorization':
                                     'Bearer ' + PRODUCER_TOKEN}
        self.director_auth_header = {'Authorization':
                                     'Bearer ' + DIRECTOR_TOKEN}
        self.database_path = DATABASE_URL

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)

        # Testing requirement - adding actors successfully
        self.post_actor1 = {
            'name': "Pranay",
            'age': 31,
            'gender': 'MALE'
        }

        self.post_actor2 = {
            'name': "Boom",
            'age': 19,
            'gender': 'FEMALE'
        }

        self.post_actor3 = {
            'name': "TestActor",
            'age': 25,
            'gender': 'MALE'
        }

        self.post_actor_missing_attr_gender = {
            'age': 18,
            'name': "NoAgeActor"
        }

        self.post_actor_missing_attr_name = {
            'age': 31,
            'gender': "FEMALE"
        }
        self.patch_actors_age = {
            'age': 19
        }

        self.post_movie1 = {
            'title': "MY LIFE",
            'release_date': "2030-03-02"
        }

        self.post_movie2 = {
            'title': "MY DOG",
            'release_date': "2045-04-03"
        }

        self.post_movie3 = {
            'title': "MR CAT",
            'release_date': "2050-06-11"
        }

        self.post_movie_title_attr_missing = {
            'release_date': "2055-02-02"
        }

        self.post_movie_release_date_attr_missing = {
            'title': "MR DOG"
        }

        self.patch_movie_on_release_date = {
            'release_date': "2035-10-10"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

# /actors test cases
# Assistant Role - GET successful
    def test_get_actors_assistant(self):
        result = self.client().get('/actors?page=1',
                            headers=self.assistant_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# Producer Role - GET successful
    def test_get_actors_producer(self):
        result = self.client().get('/actors?page=1', headers=self.producer_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# Director Role - GET successful
    def test_get_actors_director(self):
        result = self.client().get('/actors?page=1',
                            headers=self.director_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# Producer Role - POST successful
    def test_post_actors_producer(self):
        result = self.client().post('/actors',
                                json=self.post_actor1,
                                headers=self.producer_auth_header)
        data = json.loads(result.data)
        actor = Actors.query.filter_by(id=data['actor_added']).one_or_none()
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

# Director Role - POST successful
    def test_post_actors_director(self):
        result = self.client().post('/actors',
                                 json=self.post_actor2,
                                 headers=self.director_auth_header)
        data = json.loads(result.data)
        actor = Actors.query.filter_by(id=data['actor_added']).one_or_none()
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

# Director Role - PATCH successful
    def test_patch_actor_director(self):
        result = self.client().patch('/actors/2',
                                  json=self.patch_actors_age,
                                  headers=self.director_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_updated'], 2)

# Director Role - DELETE sccessful
    def test_delete_actor_director(self):
        result = self.client().post('/actors', json=self.post_actor,
                                 headers=self.director_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        actor_id = data['actor_added']
        result = self.client().delete('/actors/{}'.format(actor_id),
                                   headers=self.director_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_deleted'], actor_id)


# Director role - Actor with missing gender - POST failure
    def test_post_new_actor_with_missing_gender(self):
        result = self.client().post('/actors',
                                 json=self.post_actor_missing_attr_gender,
                                 headers=self.director_auth_header)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# Director role - Actor with missing name - POST failure
    def test_post_new_actor_with_missing_name(self):
        result = self.client().post('/actors',
                                 json=self.post_actor_missing_attr_name,
                                 headers=self.director_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# Director role - Updating age of non-existant Actor - PATCH failure
    def test_patch_invalid_actor(self):
        result = self.client().patch('/actors/99',
                                  json=self.patch_actors_age,
                                  headers=self.director_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# Director role - Actor not found - DELETE failure
    def test_delete_actor_not_found(self):
        result = self.client().delete('/actors/500',
                                   headers=self.director_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# /movies test cases
# Assistant Role - GET successful
    def test_get_movies_assistant(self):
        result = self.client().get('/movies?page=1', headers=self.assistant_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# Producer Role - GET successful
    def test_get_movies_producer(self):
        result = self.client().get('/movies?page=1', headers=self.producer_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# Director Role - GET successful
    def test_get_movies_director(self):
        result = self.client().get('/movies?page=1', headers=self.director_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# Producer Role - POST successful
    def test_post_new_movie_producer(self):
        result = self.client().post('/movies', json=self.post_movie1,
                                 headers=self.producer_auth_header)
        data = json.loads(result.data)
        movie = Movies.query.filter_by(id=data['movie_added']).one_or_none()
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(movie)

# Director Role - Update release date - PATCH successful
    def test_patch_movie_update_date_diretor(self):
        result = self.client().patch('/movies/2',
                                  json=self.patch_movie_on_release_date,
                                  headers=self.director_auth_header)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_updated'], 2)

# Producer Role - DELETE successful 
    def test_delete_movie_producer(self):
        result = self.client().post('/movies',
                                 json=self.post_movie2,
                                 headers=self.producer_auth_header)
        data = json.loads(result.data)
        movie_id = data['movie-added']
        result = self.client().delete('/movies/{}'.format(movie_id), headers=self.producer_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_deleted'], movie_id)

# Producer Role - missing title - POST unsuccessful 
    def test_post_new_movie_without_title(self):
        result = self.client().post('/movies',
                                 json=self.post_movie_title_attr_missing,
                                 headers=self.producer_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# Producer Role - missing date - POST unsuccessful 
    def test_post_new_movie_without_date(self):
        result = self.client().post('/movies',
                                 json=self.post_movie_release_date_attr_missing,
                                 headers=self.producer_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# Director Role - invalid movie id - PATCH unsucessful
    def test_patch_movie_indalid_id(self):
        result = self.client().patch('/movies/500',
                                  json=self.patch_movie_on_release_date,
                                  headers=self.director_auth_header)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# Producer Role - invalid id - DELETE unsuccessful 
    def test_delete_movie_invalid_id(self):
        result = self.client().delete('/movies/500',
                                   headers=self.producer_auth_header)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')


# RBAC Tests for /actors
# GET actors without Authorization header
    def test_fetch_actors_without_header(self):
        result = self.client().get('/actors?page=1')
        actorData = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(actorData['success'])
        self.assertEqual(actorData['message'], 'Authorization header is expected.')

# POST actors with unauthorized header (i.e. assistant role)
    def test_post_actor_with_uauthorized_header(self):
        result = self.client().post('/actors',
                                 json=self.post_actor1,
                                 headers=self.assistant_auth_header)
        actorData = json.loads(result.data)
        self.assertEqual(result.status_code, 403)
        self.assertFalse(actorData['success'])
        self.assertEqual(actorData['message'], 'Permission not found.')

# DELETE valid actor with unauthorized header (i.e assistant role)
    def test_delete_actor_with_unauthorized_header(self):
        result = self.client().delete('/actors/10', headers=self.assistant_auth_header)
        actorData = json.loads(result.data)
        self.assertEqual(result.status_code, 403)
        self.assertFalse(actorData['success'])
        self.assertEqual(actorData['message'], 'Permission not found.')

# RBAC Tests for /movies
# GET movies without Authorization header
    def test_fetch_movies_without_header(self):
        result = self.client().get('/movies?page=1')
        movieData = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(movieData['success'])
        self.assertEqual(movieData['message'], 'authorization_header_missing')

# POST movies with wrong Authorization header (i.e. director Role)
    def test_post_movie_with_unauthorized_header(self):
        result = self.client().post('/movies', json=self.post_movie1,
                                 headers=self.director_auth_header)
        movieData = json.loads(result.data)
        self.assertEqual(result.status_code, 403)
        self.assertFalse(movieData['success'])
        self.assertEqual(movieData['message'], 'Permission not found')

# DELETE existing movie witho unauthrorized header (i.e. director Role)
    def test_delete_movie_with_unauthorized_header(self):
        resultes = self.client().delete('/movies/8',
                                   headers=self.director_auth_header)
        movieData = json.loads(result.data)
        self.assertEqual(result.status_code, 403)
        self.assertFalse(movieData['success'])
        self.assertEqual(movieData['message'], 'Permission not found')


if __name__ == "__main__":
    unittest.main()