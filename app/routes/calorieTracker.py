from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from ..auth import *
from ..models import User, db, Food, Daily_Food, Meal
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
    body = request.json
    food_ids = body['food_ids']
    to = body['from']

    date = datetime.datetime(body['day'][0], body['day'][1], body['day'][2])
    daily_food = Daily_Food.query.filter_by(
        user_id=body['user_id'], day=date).first()
    # check if date exist for user; if not creat a new date
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

    return {'foods': food_list, 'food_ids': food_ids}


def getFoods(section, daily_food):
    foodList = []
    foodIds = daily_food[section]
    print(foodIds, 'foodIds')
    if (foodIds and len(foodIds) > 0):
        foodSet = set(foodIds)
        count = {}
        for foodId in foodSet:
            count[foodId] = foodIds.count(foodId)
        print(count, 'food count')
        for foodId, servings in count.items():
            food = Food.query.get(foodId)
            foodList.append({'food': food.toDict(), 'servings': servings})
    return foodList


@bp.route('user/<int:id>/foods', methods=['PATCH'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def getCalorieTrackerFoods(id):
    # date
    body = request.json
    date = datetime.datetime(body['day'][0], body['day'][1], body['day'][2])
    daily_food = Daily_Food.query.filter_by(user_id=id, day=date).first()

    if(not daily_food):
        return {'breakfast_foods': [], 'breakfast_foods_ids': [],
                'lunch_foods': [], 'lunch_foods_ids': [],
                'dinner_foods': [], 'dinner_foods_ids': [],
                'snack_foods': [], 'snack_foods_ids': []}

    # get breakfast
    breakfast_foods_list = getFoods('breakfast_foods', daily_food)
    breakfast_foods = daily_food.breakfast_foods

    # if(breakfast_foods and len(breakfast_foods) > 0):
    #     breakfastSet = set(breakfast_foods)
    #     count = {}
    #     for food in breakfastSet:
    #         count[food] = breakfast_foods.count(food)
    #     for foodId, servings in count.items():
    #         food = Food.query.get(foodId)
    #         breakfast_foods_list.append({'food': food.toDict(), 'servings': servings})
    # else:
    #     breakfast_foods = []
    # get lunch
    lunch_foods_list = getFoods('lunch_foods', daily_food)
    lunch_foods = daily_food.lunch_foods

    # if(lunch_foods and len(lunch_foods) > 0):
    #     lunchSet = set(lunch_foods)
    #     count = {}
    #     for food in lunchSet:
    #         count[food] = lunch_foods.count(food)
    #     for foodId, servings in count.items():
    #         food = Food.query.get(foodId)
    #         lunch_foods_list.append({'food': food.toDict(), 'servings': servings})
    # else:
    #     lunch_foods = []
    # get dinner
    dinner_foods_list = getFoods('dinner_foods', daily_food)
    dinner_foods = daily_food.dinner_foods

    # if(dinner_foods and len(dinner_foods) > 0):
    #     dinnerSet = set(dinner_foods)
    #     count = {}
    #     for food in dinnerSet:
    #         count[food] = dinner_foods.count(food)
    #     for foodId, servings in count.items():
    #         food = Food.query.get(foodId)
    #         dinner_foods_list.append({'food': food.toDict(), 'servings': servings})
    # else:
    #     dinner_foods=[]
    # get snack
    snack_foods_list = getFoods('snack_foods', daily_food)
    snack_foods = daily_food.snack_foods

    # if(snack_foods and len(snack_foods) > 0):
    #     snackSet = set(snack_foods)
    #     count = {}
    #     for food in snackSet:
    #         count[food] = snack_foods.count(food)
    #     for foodId, servings in count.items():
    #         food = Food.query.get(foodId)
    #         snack_foods_list.append({'food': food.toDict(), 'servings': servings})
    # else:
    #     snack_foods = []
    return {'breakfast_foods': breakfast_foods_list, 'breakfast_foods_ids': breakfast_foods,
            'lunch_foods': lunch_foods_list, 'lunch_foods_ids': lunch_foods,
            'dinner_foods': dinner_foods_list, 'dinner_foods_ids': dinner_foods,
            'snack_foods': snack_foods_list, 'snack_foods_ids': snack_foods}


def addMealId(section, daily_food, db, meal, daily_food_dict):
    mealIds = []
    if daily_food_dict[section]:
        mealIds = daily_food_dict[section].copy()
    mealIds.append(meal['id'])
    daily_food[section] = mealIds
    db.session.add(daily_food)
    db.session.commit()


@bp.route('meal', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def postCalorieTrackerMeal():
    body = request.json
    to = body['from']
    error = ''

    if body['meal_id'] == '':
        return jsonify(['Please select a Meal before sumbitting'], 400)
    # check if date exist for user
    date = datetime.datetime(body['day'][0], body['day'][1], body['day'][2])
    daily_food = Daily_Food.query.filter_by(
        user_id=body['user_id'], day=date).first()

    meal = Meal.query.get(body['meal_id'])
    meal = meal.toDict()

    if(not daily_food):
        daily_food = Daily_Food(user_id=body['user_id'], day=date)
        db.session.add(daily_food)
        db.session.commit()
    daily_food_dict = daily_food.toDict()
    keyMap = to+'_meals'

    if daily_food[to+'_meals'] and meal['id'] in daily_food[to+'_meals']:
        return jsonify(f"{meal['name']} is arleady in your meals for this section", 400)

    if to == 'breakfast':
        addMealId('breakfast_meals', daily_food, db, meal, daily_food_dict)
        # breakfast_meals = []
        # if daily_food.breakfast_meals:
        #     print(daily_food.breakfast_meals)
        #     breakfast_meals = daily_food_dict['breakfast_meals'].copy()
        # if meal['id'] in breakfast_meals:
        #     return jsonify(f"{meal['name']} is arleady in breakfast meals", 400)
        # breakfast_meals.append(body['meal_id'])
        # daily_food.breakfast_meals = breakfast_meals
        # print(breakfast_meals)
        # db.session.add(daily_food)
        # db.session.commit()
    elif to == 'lunch':
        addMealId('lunch_meals', daily_food, db, meal, daily_food_dict)
        # lunch_meals = []
        # if daily_food.lunch_meals:
        #     print(daily_food.lunch_meals)
        #     lunch_meals = daily_food_dict['lunch_meals'].copy()
        # if meal['id'] in lunch_meals:
        #     return jsonify(f"{meal['name']} is arleady in lunch meals", 400)
        # lunch_meals.append(body['meal_id'])
        # daily_food.lunch_meals = lunch_meals
        # print(lunch_meals)
        # db.session.add(daily_food)
        # db.session.commit()
    elif to == 'dinner':
        addMealId('dinner_meals', daily_food, db, meal, daily_food_dict)
        # dinner_meals = []
        # if daily_food.dinner_meals:
        #     print(daily_food.dinner_meals)
        #     dinner_meals = daily_food_dict['dinner_meals'].copy()
        # if meal['id'] in dinner_meals:
        #     return jsonify(f"{meal['name']} is arleady in dinner meals", 400)
        # dinner_meals.append(body['meal_id'])
        # daily_food.dinner_meals = dinner_meals
        # print(dinner_meals)
        # db.session.add(daily_food)
        # db.session.commit()
    elif to == 'snack':
        addMealId('snack_meals', daily_food, db, meal, daily_food_dict)
        # snack_meals = []
        # if daily_food.snack_meals:
        #     print(daily_food.snack_meals)
        #     snack_meals = daily_food_dict['snack_meals'].copy()
        # if meal['id'] in snack_meals:
        #     return jsonify(f"{meal['name']} is arleady in snack meals", 400)
        # snack_meals.append(body['meal_id'])
        # daily_food.snack_meals = snack_meals
        # print(snack_meals)
        # db.session.add(daily_food)
        # db.session.commit()

    food_ids = meal['food_ids']
    food_ids_set = set(food_ids)

    count = {}
    meal_item = {'id': meal['id'], 'name': meal['name'], 'foods': [], 'total_cal': 0,
                 'total_carbs': 0, 'total_fat': 0, 'total_protein': 0, 'food_ids': meal['food_ids']}
    for food in food_ids_set:
        count[food] = food_ids.count(food)
    for foodId, servings in count.items():
        final_food = Food.query.get(foodId)
        final_food = final_food.toDict()
        meal_item['total_cal'] += final_food['total_cal']*servings
        meal_item['total_carbs'] += final_food['total_carbs']*servings
        meal_item['total_fat'] += final_food['total_fat']*servings
        meal_item['total_protein'] += final_food['protein']*servings
        meal_item['foods'].append({**final_food, 'servings': servings})

    if error == '':
        return jsonify(meal_item, 200)
    else:
        return jsonify(error, 400)


def getMeals(daily_food, section):
    meals = []
    for mealId in daily_food[section]:
        meal = Meal.query.get(mealId)
        foodIds = meal.food_ids
        meal = meal.toDict()

        foodIdsSet = set(foodIds)
        count = {}
        meal_item = {'id': meal['id'], 'name': meal['name'], 'foods': [
        ], 'total_cal': 0, 'total_carbs': 0, 'total_fat': 0, 'total_protein': 0, 'food_ids': meal['food_ids']}

        for foodId in foodIdsSet:
            count[foodId] = foodIds.count(foodId)

        for foodId, servings in count.items():
            food = Food.query.get(foodId)
            food = food.toDict()
            meal_item['total_cal'] += food['total_cal']*servings
            meal_item['total_carbs'] += food['total_carbs']*servings
            meal_item['total_fat'] += food['total_fat']*servings
            meal_item['total_protein'] += food['protein']*servings
            meal_item['foods'].append({**food, 'servings': servings})
        meals.append(meal_item)

    return meals


@bp.route('user/<int:id>/meals', methods=['PATCH'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def getCalorieTrackerMeals(id):
    # date
    body = request.json
    date = datetime.datetime(body['day'][0], body['day'][1], body['day'][2])
    daily_food = Daily_Food.query.filter_by(user_id=id, day=date).first()

    meal_res = {'breakfast_meals': [], 'lunch_meals': [],
                'dinner_meals': [], 'snack_meals': []}
    if(not daily_food):
        return jsonify(meal_res, 200)

    if daily_food.breakfast_meals:
        meal_res['breakfast_meals'] = getMeals(daily_food, 'breakfast_meals')
        # for meal_id in daily_food.breakfast_meals:
        #     meal = Meal.query.get(meal_id)
        #     food_ids = meal.food_ids
        #     meal = meal.toDict()

        #     food_ids_set = set(food_ids)
        #     count = {}
        #     meal_item = {'id': meal['id'], 'name': meal['name'], 'foods': [
        #     ], 'total_cal': 0, 'total_carbs': 0, 'total_fat': 0, 'total_protein': 0, 'food_ids': meal['food_ids']}
        #     for food in food_ids_set:
        #         count[food] = food_ids.count(food)
        #     for foodId, servings in count.items():
        #         final_food = Food.query.get(foodId)
        #         final_food = final_food.toDict()
        #         meal_item['total_cal'] += final_food['total_cal']*servings
        #         meal_item['total_carbs'] += final_food['total_carbs']*servings
        #         meal_item['total_fat'] += final_food['total_fat']*servings
        #         meal_item['total_protein'] += final_food['protein']*servings
        #         meal_item['foods'].append({**final_food, 'servings': servings})
        #     meal_res['breakfast_meals'].append(meal_item)

    if daily_food.lunch_meals:
        meal_res['lunch_meals'] = getMeals(daily_food, 'lunch_meals')
        # for meal_id in daily_food.lunch_meals:
        #     meal = Meal.query.get(meal_id)
        #     food_ids = meal.food_ids
        #     meal = meal.toDict()

        #     food_ids_set = set(food_ids)
        #     count = {}
        #     meal_item = {'id': meal['id'], 'name': meal['name'], 'foods': [
        #     ], 'total_cal': 0, 'total_carbs': 0, 'total_fat': 0, 'total_protein': 0, 'food_ids': meal['food_ids']}
        #     for food in food_ids_set:
        #         count[food] = food_ids.count(food)
        #     for foodId, servings in count.items():
        #         final_food = Food.query.get(foodId)
        #         final_food = final_food.toDict()
        #         meal_item['total_cal'] += final_food['total_cal']*servings
        #         meal_item['total_carbs'] += final_food['total_carbs']*servings
        #         meal_item['total_fat'] += final_food['total_fat']*servings
        #         meal_item['total_protein'] += final_food['protein']*servings
        #         meal_item['foods'].append({**final_food, 'servings': servings})
        #     meal_res['lunch_meals'].append(meal_item)

    if daily_food.dinner_meals:

        meal_res['dinner_meals'] = getMeals(daily_food, 'dinner_meals')
        # for meal_id in daily_food.dinner_meals:
        #     meal = Meal.query.get(meal_id)
        #     food_ids = meal.food_ids
        #     meal = meal.toDict()

        #     food_ids_set = set(food_ids)
        #     count = {}
        #     meal_item = {'id': meal['id'], 'name': meal['name'], 'foods': [
        #     ], 'total_cal': 0, 'total_carbs': 0, 'total_fat': 0, 'total_protein': 0, 'food_ids': meal['food_ids']}
        #     for food in food_ids_set:
        #         count[food] = food_ids.count(food)
        #     for foodId, servings in count.items():
        #         final_food = Food.query.get(foodId)
        #         final_food = final_food.toDict()
        #         meal_item['total_cal'] += final_food['total_cal']*servings
        #         meal_item['total_carbs'] += final_food['total_carbs']*servings
        #         meal_item['total_fat'] += final_food['total_fat']*servings
        #         meal_item['total_protein'] += final_food['protein']*servings
        #         meal_item['foods'].append({**final_food, 'servings': servings})
        #     meal_res['dinner_meals'].append(meal_item)

    if daily_food.snack_meals:
        meal_res['snack_meals'] = getMeals(daily_food, 'snack_meals')
        # for meal_id in daily_food.snack_meals:
        #     meal = Meal.query.get(meal_id)
        #     food_ids = meal.food_ids
        #     meal = meal.toDict()

        #     food_ids_set = set(food_ids)
        #     count = {}
        #     meal_item = {'id': meal['id'], 'name': meal['name'], 'foods': [
        #     ], 'total_cal': 0, 'total_carbs': 0, 'total_fat': 0, 'total_protein': 0, 'food_ids': meal['food_ids']}
        #     for food in food_ids_set:
        #         count[food] = food_ids.count(food)
        #     for foodId, servings in count.items():
        #         final_food = Food.query.get(foodId)
        #         final_food = final_food.toDict()
        #         meal_item['total_cal'] += final_food['total_cal']*servings
        #         meal_item['total_carbs'] += final_food['total_carbs']*servings
        #         meal_item['total_fat'] += final_food['total_fat']*servings
        #         meal_item['total_protein'] += final_food['protein']*servings
        #         meal_item['foods'].append({**final_food, 'servings': servings})
        #     meal_res['snack_meals'].append(meal_item)

    return jsonify(meal_res, 200)
