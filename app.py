from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['covid_vaccination']
users_collection = db['users']
centres_collection = db['vaccination_centres']


@app.route('/users/signup', methods=['POST'])
def user_signup():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = {
        "username": username,
        "password": password
    }
    users_collection.insert_one(user)

    return jsonify(message="User registered successfully."), 201


@app.route('/users/login', methods=['POST'])
def user_login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = users_collection.find_one({"username": username, "password": password})
    if user:
        return jsonify(message="Logged in successfully.", user=user), 200
    else:
        return jsonify(message="Invalid username or password."), 401


@app.route('/centres', methods=['GET'])
def get_vaccination_centres():
    centres = list(centres_collection.find({}, {"_id": 0}))
    return jsonify(centres), 200


@app.route('/centres/apply', methods=['POST'])
def apply_vaccination_slot():
    data = request.get_json()
    centre_name = data['centre_name']

    centre = centres_collection.find_one({"name": centre_name})
    if centre and centre['slots_available'] > 0:
        centres_collection.update_one({"name": centre_name}, {"$inc": {"slots_available": -1}})
        return jsonify(message="Vaccination slot applied successfully."), 200
    else:
        return jsonify(message="No slots available for this centre."), 400


if __name__ == '__main__':
    app.run()
