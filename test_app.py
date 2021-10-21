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
        ASSISTANT_TOKEN = ''
        PRODUCER_TOKEN = ''
        DIRECTOR_TOKEN = ''

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