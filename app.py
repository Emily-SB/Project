from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
from PIL import Image
import io
import os
import requests

import firebase_admin
from firebase_admin import credentials, auth, firestore
firebase_api_key = os.getenv("FIREBASE_API_KEY")

cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load environment variables

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Dummy admin credentials (temporary until Firebase handles this)
ADMIN_CREDENTIALS = {'username': 'Emil', 'password': '123'}

# Story generation from image
def generate_story(image_data):
    try:
        image = Image.open(io.BytesIO(image_data))

        story_prompt = """
        Analyze the image carefully. Identify the main subject and describe its surroundings.
        Then, generate an engaging yet fact-based narrative about the subject. Also provide an apt title to the story.

        - If the subject is a living being (animal, plant, human), provide scientific facts about its characteristics, behavior, and significance in nature or human culture.  
        - If the subject is a non-living object (e.g., an apple, a book, a clock), narrate its journey or significance in a way that incorporates real-world facts.  
        - If the subject is something abstract or unclear, provide a general historical or scientific context related to what is visible and form a meaningful, fact-based narrative around it.  

        Ensure the response is informative but also engaging, like an educational tale rather than pure fiction.
        """

        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([story_prompt, image])
        return response.text if response else "No response generated."

    except Exception as e:
        print("Error generating story:", e)
        return "An error occurred while generating the story."

# MOVE THIS OUTSIDE!
import uuid
def save_story_to_file(story_text):
    filename = f"{uuid.uuid4().hex}.txt"
    folder = os.path.join("static", "stories")
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(story_text)

    return f"/static/stories/{filename}"

# Home redirects to login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Signup - No DB for now
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data['email']
    password = data['password']
    username = data.get('username')

    try:
        user = auth.create_user(email=email, password=password)
        # Optionally store extra info like username in Firestore
        db = firestore.client()
        db.collection('users').document(user.uid).set({
            'username': username,
            'email': email
        })
        return jsonify({"success": True, "message": "Signup successful. Please log in."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

ADMIN_CREDENTIALS = {'username': 'Emil', 'password': '123'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Admin login (handled manually)
        if email == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
            session['user'] = 'admin'  # Set session for admin
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard

        # Firebase Auth login
        try:
            # Verify user credentials with Firebase using the Firebase REST API
            user = auth.get_user_by_email(email)  # Check if email exists
            # You cannot directly validate the password in Flask with Firebase, so handle the login via Firebase client-side.
            # To verify the password, the user must log in through Firebase client-side API
            
            # If user exists in Firebase, assume it's a valid user, just redirect
            if user:
                session['user'] = user.email  # Store Firebase user email in session
                return redirect(url_for('profile'))  # Redirect to user profile/dashboard
            else:
                return "Invalid credentials", 400
        except auth.AuthError as e:
            return f"Authentication error: {str(e)}", 400

    return render_template('login.html')
# User homepage
@app.route('/homepage')
def homepage():
    if 'user' not in session or session['user'] == 'admin':
        return redirect(url_for('login'))
    return render_template('index.html', username=session['user'])

# User profile
@app.route('/profile')
def profile():
    if 'user' not in session or session['user'] == 'admin':
        return redirect(url_for('login'))
    return render_template('profile.html', username=session['user'])

# Admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Image-based story generation
from datetime import datetime
# Story saving
def save_story_to_file(story_text):
    ...

# Allowed image formats
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/generate_story', methods=['POST'])
def generate():
    if 'user' not in session or session['user'] == 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(image_file.filename):
        return jsonify({'error': 'Unsupported file format. Please upload a JPG, PNG, or WebP image.'}), 400

    try:
        image_data = image_file.read()
        story_text = generate_story(image_data)

        # Save the story to a file
        story_path = save_story_to_file(story_text)
        story_url = request.host_url.rstrip('/') + story_path

        # Save metadata to Firestore
        user_email = session['user']
        story_metadata = {
            'url': story_url,
            'timestamp': datetime.utcnow()
        }

        user_doc = db.collection('users').where('email', '==', user_email).get()
        if user_doc:
            user_id = user_doc[0].id
            db.collection('users').document(user_id).collection('stories').add(story_metadata)

        return jsonify({'story_url': story_url})
    
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Something went wrong while processing the image.'}), 500
if __name__ == '__main__':
    app.run(debug=True)