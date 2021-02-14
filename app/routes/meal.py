from flask import Blueprint, jsonify, request, g
from flask_cors import cross_origin
from ..auth import *
from ..models import User, db, Food, Meal
from sqlalchemy.orm import joinedload

bp = Blueprint("meal", __name__, url_prefix="/meal")


@bp.route('', methods=['POST'])
def postMeal():
    '''
    {
        name: string,
        food_ids: [food.id, ...],
    }
    '''
    body = request.json
    errors = []
    food_ids_set = set(body["food_ids"])

    if body["name"] == '':
        errors.append('Please enter a name')
    if len(body["food_ids"]) == 0:
        errors.append('Please Select foods')
    if len(food_ids_set) < 2:
        errors.append('Please select more than one food')

    if len(errors) > 0:
        return jsonify(errors, 400)
    else:
        meal = Meal(**body)
        db.session.add(meal)
        db.session.commit()
        meal = meal.toDict()
        print(meal)
        meal_item = {'id': meal['id'], 'name': meal['name'], 'foods': [
        ], 'total_cal': 0, 'total_carbs': 0, 'total_fat': 0, 'total_protein': 0}
        food_ids = meal['food_ids']
        food_ids_set = set(food_ids)
        count = {}

        # get a count of how many times we encounter a food id => {foodId: count}
        for food in food_ids_set:
            count[food] = food_ids.count(food)

        # tally up the total nutritional facts for the meal and add the food for the meal
        for foodId, servings in count.items():
            convertFoodId(foodId, servings, meal_item)

        return jsonify(meal_item, 200)

# meal_list =  [{id: 1, name: Carb up, foods:[{name:bok choy, servings}]}]
# returns all the meals for a given user


@bp.route('/user/<int:id>')
def getMeals(id):
    user = User.query.options(joinedload(User.meals)).get(id)
    meals = [meal.toDict() for meal in user.meals]

    meal_list = []
    for meal in meals:
        meal_item = {'id': meal['id'], 'name': meal['name'], 'foods': [], 'total_cal': 0,
                     'total_carbs': 0, 'total_fat': 0, 'total_protein': 0, 'food_ids': meal['food_ids']}
        food_ids = meal['food_ids']
        food_ids_set = set(food_ids)
        count = {}

        # get a count of how many times we encounter a food id => {foodId: count}
        for food in food_ids_set:
            count[food] = food_ids.count(food)

        # tally up the total nutritional facts for the meal and add the food for the meal
        for foodId, servings in count.items():
            convertFoodId(foodId, servings, meal_item)

        meal_list.append(meal_item)

    return jsonify(meal_list, 200)


def convertFoodId(foodId, servings, meal_item):
    final_food = Food.query.get(foodId)
    final_food = final_food.toDict()
    meal_item['total_cal'] += final_food['total_cal']*servings
    meal_item['total_carbs'] += final_food['total_carbs']*servings
    meal_item['total_fat'] += final_food['total_fat']*servings
    meal_item['total_protein'] += final_food['protein']*servings
    meal_item['foods'].append({**final_food, 'servings': servings})
