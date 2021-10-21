import os
from unittest import result
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actors, Movies
from auth import AuthError, requires_auth

RECORDS_PER_PAGE = 10

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

# Pagination function for better display
# source: Own code from trivia API
# https://github.com/pranay22/Trivia-Api-Webdev-nanodegree/blob/main/backend/flaskr/__init__.py
    def paginate_view(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * RECORDS_PER_PAGE
        end = start + RECORDS_PER_PAGE
        items = [item.format() for item in selection]
        paginated_items = items[start:end]
        return paginated_items

# Endpoint for testing the app, whether it is running or not
    @app.route('/', methods={'GET'})
    def home():
        return jsonify({
            'success': True,
            'message': 'Healthy'
        })

    '''
    GET method for /actors
    Fetches all actor details
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth(permission='get:actors-detail')
    def get_actors(payload):
        try:
            actors = Actors.query.order_by(Actors.id).all()
            paged_actors = paginate_view(request, actors)
            total_actors = len(actors)
            result = {
                'success': True,
                'actors': paged_actors,
                'total-actors': total_actors
            }
            # returning HTTP 200 explicitly
            return jsonify(result), 200
        except Exception:
            abort(422) 

    '''
    POST method for /actors
    it can create new row in actors table
    requires 'post:actors' permission
    returns HTT 200 for valid post or other status messages for exceptions
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:actors')
    def post_actors(payload):
        # fetch Input
        if request.data:
            inputReqData = request.get_json()
            try:
                new_actor = Actors()
                new_actor.name = inputReqData.get('name')
                new_actor.gender = inputReqData.get('gender')
                new_actor.age = inputReqData.get('age')
                new_actor.insert()

            except Exception:
                abort(400)

            result = {
                "success": True,
                "actor_added": new_actor.id
            }
            return jsonify(result), 200


    # Error Handling for HTTP400, 401, 403, 404, 4ß5, 422, 500, authError
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