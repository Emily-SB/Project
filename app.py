from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import io
import os

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session handling

# Dummy admin credentials
ADMIN_CREDENTIALS = {'username': 'Emil', 'password': '123'}

# Function to generate a story from an image
def generate_story(image_data):
    try:
        # Convert binary data to a PIL image
        image = Image.open(io.BytesIO(image_data))

        # Define the prompt
        story_prompt = """
        Analyze the image carefully. Identify the main subject and describe its surroundings.
        Then, generate an engaging yet fact-based narrative about the subject. Also provide an apt title to the story.

        - If the subject is a living being (animal, plant, human), provide scientific facts about its characteristics, behavior, and significance in nature or human culture.  
        - If the subject is a non-living object (e.g., an apple, a book, a clock), narrate its journey or significance in a way that incorporates real-world facts.  
        - If the subject is something abstract or unclear, provide a general historical or scientific context related to what is visible and form a meaningful, fact-based narrative around it.  

        Ensure the response is informative but also engaging, like an educational tale rather than pure fiction.
        """

        # Send to the AI model
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([story_prompt, image])

        return response.text if response else "No response generated."

    except Exception as e:
        print("Error generating story:", e)
        return "An error occurred while generating the story."

# 🚀 Root Route: Redirects to login page
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"success": False, "message": "Email already registered!"})

    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Signup successful! You can now log in."})


# 🚀 Login Page: Handles both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Admin login check
        if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
            session['user'] = 'admin'
            return redirect(url_for('admin_dashboard'))  # Redirect to Admin Dashboard

        # User login (Any username/password works)
        session['user'] = username
        return redirect(url_for('homepage'))  # Redirect to Homepage

    return render_template('login.html')

# 🚀 User Homepage (After login)
@app.route('/homepage')
def homepage():
    if 'user' not in session or session['user'] == 'admin':
        return redirect(url_for('login'))  # Only users (not admin) can access
    return render_template('index.html', username=session['user'])  # Pass username to homepage

# 🚀 Profile Page (For Users)
@app.route('/profile')
def profile():
    if 'user' not in session or session['user'] == 'admin':
        return redirect(url_for('login'))  # Only normal users can access
    return render_template('profile.html', username=session['user'])

# 🚀 Admin Dashboard (For Admin)
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('login'))  # Only admin can access
    return render_template('admin.html')

# 🚀 Logout Route (Clears session and redirects to login)
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# 🚀 Story Generation API Endpoint
@app.route('/generate_story', methods=['POST'])
def generate():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Read the image as binary data
    image_data = image_file.read()

    # Generate the story
    story = generate_story(image_data)

    return jsonify({'story': story})

# 🚀 Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
   