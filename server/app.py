#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

@app.route("/")
def home():
    return '<h1>Camping Fun</h1>'


class Campers(Resource):
    def get(self):
        try:
            campers = [camper.to_dict(rules=("-signups",)) for camper in Camper.query] 
            return campers, 200
        except Exception as e:
            return {"error": str(e)}, 400

    def post(self):
        try:
            data = request.json
            new_camper = Camper(**data)
            db.session.add(new_camper)
            db.session.commit()
            return new_camper.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"errors": ["validation errors"]}, 400


class CampersById(Resource):
    def get(self, id):
        try: 
            if camper := db.session.get(Camper, id):
                return camper.to_dict(), 200
            else:
                return {"error": "Camper not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    def patch(self):
        pass


class Activities(Resource):
    def get(self):
        try:
            a = [a.to_dict(rules=('-signups',)) for a in Activity.query]
            return a, 200
        except Exception as e:
            return {"error": str(e)}, 400


class ActivitiessById(Resource):
    def delete(self):
        try:
            if activity := db.session.get(Activities, id):
                db.session.delete(activity)
                db.session.commit()
                return {}, 204
            else:
                return {"error": "Activity not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 400


class Signups(Resource):
    def post(self):
        try:
            data = request.json
            new_signup = Signup(**data)
            db.session.add(new_signup)
            db.session.commit()
            return new_signup.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"errors": ["validation errors"]}, 400


api.add_resource(Campers, "/campers")
api.add_resource(CampersById, "/campers/<int:id>")
api.add_resource(Activities, "/activities")
api.add_resource(ActivitiessById, "/activities/<int:id>")
api.add_resource(Signups, "/signups")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
