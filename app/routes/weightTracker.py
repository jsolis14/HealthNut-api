from flask import Blueprint, jsonify, request, g
from flask_cors import cross_origin
from ..auth import *
from ..models import User, db, Food, Meal, User_Weight
from sqlalchemy.orm import joinedload
import datetime

bp = Blueprint("weightTracker", __name__, url_prefix="/weight-tracker")


@bp.route('/user/<int:id>', methods=['POST'])
def postUserWeight(id):
    body = request.json
    date = datetime.datetime(body['day'][0],body['day'][1],body['day'][2])
    print(body)
    weight = User_Weight.query.filter_by(user_id=id, day=date).first()
    if (not weight):
        print('here')
        weight = User_Weight(user_id=id, weight=body['weight'], day=date)
        db.session.add(weight)
        db.session.commit()
    else:
        weight.weight = body['weight']
        db.session.add(weight)
        db.session.commit()

    return jsonify(weight.toDict(), 200)

@bp.route('/user/<int:id>')
def getUserWeight(id):
    body = request.json
    print(body)
    weights = User_Weight.query.filter_by(user_id=id).order_by(User_Weight.day).all()


    weight_list = [weight.toDict() for weight in weights]
    return jsonify(weight_list, 200)

@bp.route('/user/<int:id>', methods=['PATCH'])
def getUserWeightByDay(id):
    body = request.json
    date = datetime.datetime(body['day'][0],body['day'][1],body['day'][2])
    weight = User_Weight.query.filter_by(user_id=id, day=date).first()

    if(weight):
        return jsonify(weight.toDict(), 200)
    else:
        return jsonify('resource not found', 204)
