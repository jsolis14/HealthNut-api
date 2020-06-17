from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    nickname = db.Column(db.String)
    name = db.Column(db.String)
    body_weight = db.Column(db.Float)
    gender = db.Column(db.String)
    height = db.Column(db.Float)
    age = db.Column(db.Integer)
    activity_factor = db.Column(db.String)

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
        }
