# app.py for dating app
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from user import User
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client["Fair"]
activity_log = db["Activity Log"]
users = db["Users"]
matches = db["Matches"]
messages = db["Messages"]
profiles = db["Profiles"]
block = db["Block"]


def test_functions():
    db.activity_log.insert_one({"key": "value"})
    # Test get
    #document = db["Activity Log"].find_one({"key": "value"})
    # Test add
    #db["Activity Log"].update_one({"key": "value"}, {"$set": {"key2": "value2"}})
    # Test remove
    #db["Activity Log"].delete_one({"key": "value"})
    return "Test completed successfully."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_mongodb_functions')
def test_mongodb_functions():
    # Implement test functions here
    result = test_functions()
    return result

@app.route("/edit-profile")
def edit_profile():
    return render_template('edit-profile.html')

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    
    if db.users.find_one({'username': username}):
        return jsonify({'message': 'User already exists'}), 400
    
    user = User(username, password)
    db.users.insert_one({'username': user.username, 'password': user.password})
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = db.users.find_one({'username': username})
    
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
    
    return jsonify({'token': token.decode('UTF-8')}), 200

# Example protected route
@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'message': 'Token is missing'}), 401
    
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'])
        username = payload['username']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    
    return jsonify({'message': f'Welcome, {username}!'}), 200

if __name__ == '__main__':
    app.run(debug=True)