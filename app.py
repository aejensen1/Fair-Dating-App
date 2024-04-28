# app.py for dating app
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask_login import LoginManager, login_user, current_user, UserMixin, login_required, logout_user
from dotenv import load_dotenv
import os
from bson import ObjectId
from bson.errors import InvalidId

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
login_manager = LoginManager(app)

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client["Fair"]
activity_log = db["Activity Log"]
users = db["Users"]
matches = db["Matches"]
messages = db["Messages"]
profiles = db["Profiles"]
block = db["Block"]

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id # Use MongoDB's _id field as the id attribute
        self.username = username
        self.password_hash = password_hash


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    try:
        # Attempt to convert user_id to ObjectId
        user_obj_id = ObjectId(user_id)
    except InvalidId:
        # If user_id cannot be converted to ObjectId, return None
        return None
    
    # Query the user from the database
    user_data = users.find_one({'_id': user_obj_id})
    if user_data:        
        return User(id=str(user_data['_id']), username=user_data['username'], password_hash=user_data['password'])
    else:
        return None

@app.route('/')
def index():
    return render_template('login.html', current_user=current_user)

@app.route('/test_mongodb_functions', methods=['GET', 'POST'])
def test_mongodb_functions():
    if request.method == 'POST':
        activity_log.insert_one({"key": "value"})
        return "Test completed successfully."
    else:
        return render_template('index2.html')

@app.route("/edit-profile")
def edit_profile():
    return render_template('edit-profile.html')

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route('/home')
@login_required
def home():
    # Render the home page template or perform necessary actions
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            username = data.get('username')
            password = data.get('password')
        else:
            # If the content type is not JSON, assume form data
            username = request.form.get('username')
            password = request.form.get('password')
        
        # Check if username or password is missing
        if not username or not password:
            return jsonify({'message': 'Missing username or password'}), 400

        # Check if username already exists
        if users.find_one({'username': username}):
            return jsonify({'message': 'Username already exists'}), 400

        # Hash the password before storing it
        password_hash = generate_password_hash(password)

        # Generate an ObjectId for the user ID
        user_id = ObjectId()

        # Insert the user document and get the inserted ID
        result = users.insert_one({'_id': user_id, 'username': username, 'password': password_hash})
        
        # Create the user object with the correct ID
        user = User(id=user_id, username=username, password_hash=password_hash)
        
        # Automatically log in the user after registration
        login_user(user)

        return redirect(url_for('home'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            username = data.get('username')
            password = data.get('password')
        else:
            # If the content type is not JSON, assume form data
            username = request.form.get('username')
            password = request.form.get('password')
        
        if not username or not password:
            return jsonify({'message': 'Missing username or password'}), 400
        
        user_data = users.find_one({'username': username})
        
        if not user_data or not check_password_hash(user_data['password'], password):
            return jsonify({'message': 'Invalid username or password'}), 401
        
        # Create a user instance from the retrieved user data
        user = User(id=user_data['_id'], username=user_data['username'], password_hash=user_data['password'])
        
        # Log in the user
        login_user(user)

        token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
        
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    # Log out the user
    return redirect(url_for('login'))

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