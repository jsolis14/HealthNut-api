from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from ..auth import *
from ..models import User, db, Food, Daily_Food
import datetime
bp = Blueprint("calorieTracker", __name__, url_prefix="/calorie-tracker")

@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@bp.route('/foods', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def postCalorieTrackerFoods():
    # date
    # breakfast_foods
    # breakfast_meals
    # lunch_foods
    # lunch_meals
    # dinner_foods
    # dinner_meals
    # snack_foods
    # snack_meals
    # user_id
    body = request.json
    breakfast_foods = body['breakfast_foods']
    # check if date exist for user
    date = datetime.datetime(body['day'][0],body['day'][1],body['day'][2])
    daily_food = Daily_Food.query.filter_by(user_id=body['user_id'], day=date).first()

    if(daily_food):
        pass
        print('here')
    else:
        daily_food = Daily_Food(day=date, user_id=body['user_id'])
        db.session.add(daily_food)
        db.session.commit()

    breakfast_foods_list = []
    if(len(breakfast_foods) > 0):
        breakfastSet = set(breakfast_foods)
        count = {}
        for food in breakfastSet:
            count[food] = breakfast_foods.count(food)
        for foodId, servings in count.items():
            food = Food.query.get(foodId)
            breakfast_foods_list.append({'food': food.toDict(), 'servings': servings})
        # change for later
        daily_food.breakfast_foods = body['breakfast_foods']
        db.session.add(daily_food)
        db.session.commit()
        print(count)
        print(breakfast_foods_list)
    if(len(breakfast_foods) > 0):
        pass
    if(len(breakfast_foods) > 0):
        pass
    if(len(breakfast_foods) > 0):
        pass
    print(body)

    return {'breakfast_foods': breakfast_foods_list}

@bp.route('user/<int:id>/foods', methods=['PATCH'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def getCalorieTrackerFoods(id):
    ##date
    body = request.json
    date = datetime.datetime(body['day'][0],body['day'][1],body['day'][2])
    daily_food = Daily_Food.query.filter_by(user_id=id, day=date).first()
    print(daily_food)

    ## some thoughts
    breakfast_foods_list = []
    breakfast_foods = daily_food.breakfast_foods
    if(len(breakfast_foods) > 0):
        breakfastSet = set(breakfast_foods)
        count = {}
        for food in breakfastSet:
            count[food] = breakfast_foods.count(food)
        for foodId, servings in count.items():
            food = Food.query.get(foodId)
            breakfast_foods_list.append({'food': food.toDict(), 'servings': servings})
    return {'breakfast_foods': breakfast_foods_list}
