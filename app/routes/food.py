from flask import Blueprint, jsonify, request, g
from flask_cors import cross_origin
from ..auth import *
from ..models import User, db, Food

bp = Blueprint("food", __name__, url_prefix="/food")

'''
---------------------TO DO---------------------------
- user can enter a string when it should be a number and it wouldn't catch an error
- lack of requires Auth rapper
'''


@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@bp.route('', methods=['POST'])
def postFood():
    '''
    {name: string,
    total_fat: number,
    saturated_fat: number,
    trans_fat: number,
    cholesterol: number,
    sodium: number,
    total_carbs: number,
    dietary_fiber: number,
    sugars: number,
    protein: number,
    total_cal: number}
    '''

    body = request.json
    errors = []
    name = body['name']
    total_fat = body['total_fat']
    saturated_fat = body['saturated_fat']
    trans_fat = body['trans_fat']
    cholesterol = body['cholesterol']
    sodium = body['sodium']
    total_carbs = body['total_carbs']
    dietary_fiber = body['dietary_fiber']
    sugars = body['sugars']
    protein = body['protein']
    total_cal = body['total_cal']

    if (not name or name == ''):
        errors.append('Please provide a value for name')
    if (total_fat == None or total_fat == ''):
        errors.append('Please provide a value for total fat')
    if (total_carbs == None or total_carbs == ''):
        errors.append('Please proavide a value for total carbs')
    if(total_cal == None or total_cal == ''):
        errors.append('Please provide a value for total calories')
    if(protein == None or protein == ''):
        errors.append('Please provide a value for protein')
    if(total_fat < 0 or saturated_fat < 0 or trans_fat < 0 or cholesterol < 0 or sodium < 0 or total_carbs < 0 or dietary_fiber < 0 or sugars < 0 or protein < 0 or total_cal < 0):
        errors.append('values must be greater than 0')

    if(len(errors) == 0):
        food = Food(**body)
        db.session.add(food)
        db.session.commit()
        return jsonify(food.toDict(), 201)
    else:
        return jsonify(errors, 400)
