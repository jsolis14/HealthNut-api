from six.moves.urllib.request import urlopen
from flask_migrate import Migrate
from functools import wraps
from .models import db
from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import cross_origin, CORS
from jose import jwt
from .auth import *
from .routes import users, food, calorieTracker, meal, weightTracker
import os
from flask_json_schema import JsonSchema, JsonValidationError
from .auth import *

app = Flask(__name__)
schema = JsonSchema(app)
app.config.from_mapping({
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'FLASK_ENV': os.environ.get('FLASK_ENV'),
    'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL'),
})
db.init_app(app)
Migrate(app, db)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(users.bp)
app.register_blueprint(food.bp)
app.register_blueprint(calorieTracker.bp)
app.register_blueprint(meal.bp)
app.register_blueprint(weightTracker.bp)

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]})

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
