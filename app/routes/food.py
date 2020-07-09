from flask import Blueprint, jsonify, request, g
from flask_cors import cross_origin
from ..auth import *
from ..models import User, db, Food
from flask_expects_json import expects_json

bp = Blueprint("food", __name__, url_prefix="/food")
schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'integer'},
        'total_fat': {'type': 'integer'},
        'saturated_fat': {'type': 'integer'},
        'trans_fat': {'type': 'integer'},
        'cholesterol': {'type': 'integer'},
        'sodium': {'type': 'integer'},
        'total_carbs': {'type': 'integer'},
        'dietary_fiber': {'type': 'integer'},
        'sugars': {'type': 'integer'},
        'protein': {'type': 'integer'},
        'total_cal': {'type': 'integer'},
        'name': {'type': 'string'}
    },
    'required': ['user_id', 'total_fat', 'total_carbs', 'protein', 'total_cal', 'name']
}

@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@bp.route('', methods=['POST'])
@expects_json(schema)
def postFood():
    body = request.json
    print(body)
    print(body)
    food = Food(**body)
    db.session.add(food)
    db.session.commit()
    return jsonify(food.toDict(), 201)
