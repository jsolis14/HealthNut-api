from flask import Blueprint, jsonify
from flask_cors import cross_origin
from ..auth import *
from ..models import User, db
bp = Blueprint("users", __name__, url_prefix="/users")


@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@bp.route("", methods=["PATCH"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def patch_post_user():
    body = request.json
    print(body['email'])
    user_db = User.query.filter_by(email=body["email"]).first()
    print(user_db)
    if user_db:
        user_db.nickname = body["nickname"]
        user_db.name = body["name"]
        return jsonify(user_db.toDict())
    else:
        new_user = User(email=body["email"],
                        nickname=body["nickname"],
                        name=body["name"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.toDict(), 201)

@bp.route('/updateinfo', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def updateInfo():
    body = request.json
    print(body)
    user = User.query.get(body['id'])
    user.body_weight = body['weight']
    user.gender = body['gender']
    user.height = body['height']
    user.age = body['age']
    user.activity_factor = body['activityFactor']
    user.bmr = body['bmr']
    user.cal_limit = body['calorieLimit']
    user.cal_needs = body['calorieNeeds']
    db.session.commit()
    return jsonify('', 200)
