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
    user_db = User.query.filter_by(email=body["email"]).first()
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
