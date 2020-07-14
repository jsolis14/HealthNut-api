from flask import Blueprint, jsonify, request, g
from flask_cors import cross_origin
from ..auth import *
from ..models import User, db, Food, Meal

bp = Blueprint("meal", __name__, url_prefix="/meal")


@bp.route('', methods=['POST'])
def postFood():
    body = request.json
    print(body)
    return ''
