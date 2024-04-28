# app.py for dating app
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, UserMixin, login_required, logout_user
from dotenv import load_dotenv
import os
from bson import ObjectId
from bson.errors import InvalidId
from functools import wraps

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

# Define a decorator to check if the user is authenticated
def logout_if_authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            logout_user()  # Log out the user
        return f(*args, **kwargs)
    return decorated_function

def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_view

@app.before_request
def before_request():
    if not current_user.is_authenticated and request.endpoint and request.endpoint != 'login' and request.endpoint != 'register':
        return redirect(url_for('login'))

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
    user_data = users.find_one({'_id': ObjectId(current_user.get_id())})
    username = user_data['username']
    profile_complete = user_data['profile_complete']

    # Render the home page template or perform necessary actions
    return render_template('home.html', username=username, profile_complete=profile_complete)

@app.route('/register', methods=['GET', 'POST'])
@logout_if_authenticated
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
        result = users.insert_one({'_id': user_id, 'username': username, 'password': password_hash, 'profile_complete': False})
        
        # Create the user object with the correct ID
        user = User(id=user_id, username=username, password_hash=password_hash)
        
        # Automatically log in the user after registration
        login_user(user)

        return redirect(url_for('home'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
@logout_if_authenticated
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
          
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    # Log out the user
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)