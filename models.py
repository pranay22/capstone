import os
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy
import json

from sqlalchemy.sql.expression import false, null

#database_path='postgresql://pranay:test123@localhost:5432/castagency'
database_path = os.environ['DATABASE_URL']

print(database_path)

if database_path[:10] != 'postgresql':
    database_path = database_path.replace('postgres', 'postgresql')

print(database_path)

db = SQLAlchemy()

# Setting up SQLAlchemy service for flask
# Source: Coffeeshop project from Udacity itself
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

# db_drop_and_create_all()


# tests table with Name & ID

class Test(db.Model):  
  __tablename__ = 'tests'

  id = Column(Integer(), primary_key=True)
  name = Column(String)
  test = Column(String)

  def __init__(self, name):
    self.name = name

  def format(self):
    return {
      'id': self.id,
      'name': self.name
    }

# actors table
class Actors(db.Model):
    __tablename__ = 'actors'
    # Primary key - actor ID
    id = Column(Integer, primary_key=True)
    # actor name, not null
    name = Column(String, nullable=False)
    # actor gender, not null
    gender = Column(String, nullable=False)
    # actor age, not null
    age = Column(Integer, nullable=False)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    # returns a formatted version of actor
    def format(self):
        return {
            'id': self.id,
            'name' : self.name,
            'gender': self.gender,
            'age': self.age
            }

    # insert a new actor model in database
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # update existing actors
    def update(self):
        db.session.commit()

    # deletes an actor model in the database, if it exists
    def delete(self):
        db.session.delete(self)
        db.session.commit()

# movies table
class Movies(db.Model):
    __tablename__ = 'movies'
    # Primaty key - movie ID
    id = Column(Integer, primary_key=True)
    # Movie title, not null
    title = Column(String, nullable=False)
    # Movie release date, not null
    release_date = Column(Date, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    # returns a formatted version of movie
    def format(self):
        return {
            'id': self.id,
            'title' : self.title,
            'release_date': self.release_date
            }

    # insert a movie model in database
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # update existing movies
    def update(self):
        db.session.commit()

    # deletes a movie model in the database, if it exists
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    