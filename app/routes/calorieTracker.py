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
    print(body)
    food_ids = body['food_ids']
    to = body['from']

    # check if date exist for user
    date = datetime.datetime(body['day'][0],body['day'][1],body['day'][2])
    daily_food = Daily_Food.query.filter_by(user_id=body['user_id'], day=date).first()

    if(not daily_food):
        daily_food = Daily_Food(day=date, user_id=body['user_id'])
        db.session.add(daily_food)
        db.session.commit()

    food_list = []
    if(len(food_ids) > 0):
        foods_ids_Set = set(food_ids)
        count = {}
        for food in foods_ids_Set:
            count[food] = food_ids.count(food)
        for foodId, servings in count.items():
            food = Food.query.get(foodId)
            food_list.append({'food': food.toDict(), 'servings': servings})

    if(to == 'breakfast'):
        daily_food.breakfast_foods = food_ids
        db.session.add(daily_food)
        db.session.commit()
    elif(to == 'lunch'):
        daily_food.lunch_foods = food_ids
        db.session.add(daily_food)
        db.session.commit()
    elif(to == 'dinner'):
        daily_food.dinner_foods = food_ids
        db.session.add(daily_food)
        db.session.commit()
    elif(to == 'snack'):
        daily_food.snack_foods = food_ids
        db.session.add(daily_food)
        db.session.commit()
    # breakfast_foods_list = []
    # if(len(breakfast_foods) > 0):
    #     breakfastSet = set(breakfast_foods)
    #     count = {}
    #     for food in breakfastSet:
    #         count[food] = breakfast_foods.count(food)
    #     for foodId, servings in count.items():
    #         food = Food.query.get(foodId)
    #         breakfast_foods_list.append({'food': food.toDict(), 'servings': servings})
    #     # change for later
    #     daily_food.breakfast_foods = body['breakfast_foods']
    #     db.session.add(daily_food)
    #     db.session.commit()
    #     print(count)
    #     print(breakfast_foods_list)
    # if(len(breakfast_foods) > 0):
    #     pass
    # if(len(breakfast_foods) > 0):
    #     pass
    # if(len(breakfast_foods) > 0):
    #     pass
    # print(body)

    return {'foods': food_list, 'food_ids':food_ids}

@bp.route('user/<int:id>/foods', methods=['PATCH'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def getCalorieTrackerFoods(id):
    ##date
    body = request.json
    date = datetime.datetime(body['day'][0],body['day'][1],body['day'][2])
    daily_food = Daily_Food.query.filter_by(user_id=id, day=date).first()

    if(not daily_food):
        return {'breakfast_foods': [], 'breakfast_foods_ids': [],
    'lunch_foods': [], 'lunch_foods_ids': [],
    'dinner_foods': [], 'dinner_foods_ids': [],
    'snack_foods': [], 'snack_foods_ids': []}

    print(daily_food)

    ## get breakfast
    breakfast_foods_list = []
    breakfast_foods = daily_food.breakfast_foods

    if(breakfast_foods and len(breakfast_foods) > 0):
        breakfastSet = set(breakfast_foods)
        count = {}
        for food in breakfastSet:
            count[food] = breakfast_foods.count(food)
        for foodId, servings in count.items():
            food = Food.query.get(foodId)
            breakfast_foods_list.append({'food': food.toDict(), 'servings': servings})
    else:
        breakfast_foods = []
    ##get lunch
    lunch_foods_list = []
    lunch_foods = daily_food.lunch_foods

    if(lunch_foods and len(lunch_foods) > 0):
        lunchSet = set(lunch_foods)
        count = {}
        for food in lunchSet:
            count[food] = lunch_foods.count(food)
        for foodId, servings in count.items():
            food = Food.query.get(foodId)
            lunch_foods_list.append({'food': food.toDict(), 'servings': servings})
    else:
        lunch_foods = []
    ##get dinner
    dinner_foods_list = []
    dinner_foods = daily_food.dinner_foods

    if(dinner_foods and len(dinner_foods) > 0):
        dinnerSet = set(dinner_foods)
        count = {}
        for food in dinnerSet:
            count[food] = dinner_foods.count(food)
        for foodId, servings in count.items():
            food = Food.query.get(foodId)
            dinner_foods_list.append({'food': food.toDict(), 'servings': servings})
    else:
        dinner_foods=[]
    ##get snack
    snack_foods_list = []
    snack_foods = daily_food.snack_foods

    if(snack_foods and len(snack_foods) > 0):
        snackSet = set(snack_foods)
        count = {}
        for food in snackSet:
            count[food] = snack_foods.count(food)
        for foodId, servings in count.items():
            food = Food.query.get(foodId)
            snack_foods_list.append({'food': food.toDict(), 'servings': servings})
    else:
        snack_foods = []
    return {'breakfast_foods': breakfast_foods_list, 'breakfast_foods_ids': breakfast_foods,
    'lunch_foods': lunch_foods_list, 'lunch_foods_ids': lunch_foods,
    'dinner_foods': dinner_foods_list, 'dinner_foods_ids': dinner_foods,
    'snack_foods': snack_foods_list, 'snack_foods_ids': snack_foods}
