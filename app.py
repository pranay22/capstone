import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  CORS(app)
  cors = CORS(app, resources={r"/*": {'origins': '*'}})
  # explicitly set 'Access-control-allow-headers/methods
  @app.after_request
  def after_request(response):
      response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type, Authorization'
      )
      response.headers.add(
          'Access-Control-Allow-Methods',
          'GET, POST, PATCH, DELETE, OPTIONS'
      )
      return response

  @app.route('/', methods={'GET'})
  def home():
    return jsonify({
        'success': True,
        'message': 'Healthy'
    })

    # Error Handling
    # Source: https://github.com/pranay22/Coffee-shop-fullstack-nanodegree/blob/main/backend/src/api.py
    @app.errorhandler(400)
    def errorBadRequest(error):
        errorData = {
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }
        return jsonify(errorData), 400

    @app.errorhandler(401)
    def errorUnauthorized(error):
        errorData = {
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }
        return jsonify(errorData), 401

    @app.errorhandler(403)
    def errorForbidden(error):
        errorData = {
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }
        return jsonify(errorData), 403

    @app.errorhandler(404)
    def errorNotFound(error):
        errorData = {
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }
        return jsonify(errorData), 404

    @app.errorhandler(422)
    def errorUnprocessable(error):
        errorData = {
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }
        return jsonify(errorData), 422

    @app.errorhandler(500)
    def errorInternalServer(error):
        errorData = {
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }
        return jsonify(errorData), 500

    @app.errorhandler(AuthError)
    def authError(e):
        errorData = {
            "success": False,
            "error": e.status_code,
            "message": e.description
        }
        return jsonify(errorData), e.status_code

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    # app.run()