from flask import Blueprint, jsonify
from flask_cors import cross_origin
from ..auth import *
from ..models import User, db, Food
bp = Blueprint("food", __name__, url_prefix="/food")

@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@bp.route('', methods=['POST'])
def postFood():
    body = request.json
    print(body)
    food = Food(**body)
    db.session.add(food)
    db.session.commit()
    return jsonify(food.toDict(), 201)
