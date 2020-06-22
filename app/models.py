from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    nickname = db.Column(db.String)
    name = db.Column(db.String)
    body_weight = db.Column(db.Integer)
    gender = db.Column(db.String)
    height = db.Column(db.String)
    age = db.Column(db.Integer)
    activity_factor = db.Column(db.Float)
    bmr = db.Column(db.Float)
    cal_needs = db.Column(db.Integer)
    cal_limit = db.Column(db.Integer)

    # relationships
    foods = db.relationship("Food", backref="user")
    meals = db.relationship("Meal", backref="user")
    daily_foods = db.relationship("Daily_Food", backref="user")
    user_weights = db.relationship("User_Weight", backref="user")
    daily_caloric_intakes = db.relationship("Daily_Caloric_Intake", backref="user")

    def toDict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nickname': self.nickname,
            'name': self.name,
            'body_weight': self.body_weight,
            'gender': self.gender,
            'height': self.height,
            'age': self.age,
            'activity_factor': self.activity_factor,
            'bmr' : self.bmr,
            'cal_needs' : self.cal_needs,
            'cal_limit' : self.cal_limit,
        }

class User_Weight(db.Model):
    __tablename__ = 'user_weight'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Date, nullable=False)

    def toDict(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'weight' : self.weight,
            'date' : self.date,
        }

class Daily_Caloric_Intake(db.Model):
    __tablename__ = 'daily_caloric_intake'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    day = db.Column(db.Date, nullable=False)
    calorie_limit = db.Column(db.Integer, nullable=False)
    total_cal = db.Column(db.Integer, nullable=False)
    total_fat = db.Column(db.Integer, nullable=False)
    total_cholesterol = db.Column(db.Integer, nullable=False)
    total_sodium = db.Column(db.Integer, nullable=False)
    total_carbs = db.Column(db.Integer, nullable=False)
    total_protein = db.Column(db.Integer, nullable=False)

    def toDict(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'date' : self.date,
            'calorie_limit' : self.calorie_limit,
            'total_cal' : self.total_cal,
            'total_fat' : self.total_fat,
            'total_cholesterol' : self.total_cholesterol,
            'total_sodium' : self.total_sodium,
            'total_carbs' : self.total_carbs,
            'total_protein' : self.total_protein,
        }

meals = db.Table('meals',
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id'), primary_key=True),
    db.Column('food_id', db.Integer, db.ForeignKey('foods.id'), primary_key=True)
)
class Food(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    total_fat = db.Column(db.Integer)
    saturated_fat = db.Column(db.Integer)
    trans_fat = db.Column(db.Integer)
    cholesterol = db.Column(db.Integer)
    sodium = db.Column(db.Integer)
    total_carbs = db.Column(db.Integer)
    dietary_fiber = db.Column(db.Integer)
    sugars = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    total_cal = db.Column(db.Integer)

    def toDict(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'name': self.name,
           'total_fat' : self.total_fat,
            'saturated_fat' : self.saturated_fat,
            'trans_fat' : self.trans_fat,
            'cholesterol' : self.cholesterol,
            'sodium' : self.sodium,
            'total_carbs' : self.total_carbs,
            'dietary_fiber' : self.dietary_fiber,
            'sugars' : self.sugars,
            'protein' : self.protein,
            'total_cal' : self.total_cal,
        }

class Meal(db.Model):
    __tablename__ = 'meal'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    foods = db.relationship('Food', secondary=meals, lazy='subquery', backref=db.backref('meals', lazy=True))

    def toDict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name
        }

class Daily_Food(db.Model):
    __tablename__ = 'daily_foods'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    day = db.Column(db.Date, nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey("foods.id"))
    meal_id = db.Column(db.Integer, db.ForeignKey("meal.id"))
    type = db.Column(db.String, nullable=False)

    def toDict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date,
            'food_id': self.food_id,
            'meal_id': self.meal_id,
            'type': self.type,
        }
