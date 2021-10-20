import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_path='postgresql://pranay:test123@localhost:5432/castagency'
#database_path = os.environ['DATABASE_URL']

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
