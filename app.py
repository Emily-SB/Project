from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
from PIL import Image
import io
import os
import requests
import textwrap
from datetime import datetime
# Add this with your other imports like 'from PIL import Image'
from PIL import UnidentifiedImageError
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
ADMIN_CREDENTIALS = {'username': 'test2@gmail.com', 'password': '000000'}

# Story generation from image
MODEL_NAME = "gemini-1.5-pro"
def generate_story(image_data: bytes) -> str:
    """
    Analyzes an image using Google's Gemini model and generates an engaging,
    fact-based narrative about the image's subject, along with a title.

    Args:
        image_data: A bytes object containing the image data (e.g., read from a file).

    Returns:
        A string containing the generated title and story, or an error message.
    """
    try:
        print("🔍 Trying to open the image...")
        # Use Pillow to open the image from bytes
        image = Image.open(io.BytesIO(image_data))
        # Optional: You could add image validation/resizing here if needed
        print(f"🖼️ Image opened successfully (Format: {image.format}, Size: {image.size})")

        print("🧠 Preparing prompt and initializing model...")
        story_prompt = textwrap.dedent("""
        Analyze the image carefully. Identify the main subject and describe its surroundings clearly.
        Then, generate an engaging yet fact-based narrative about the subject. Also provide an apt title for the story, formatted as:

        **Title:** [Your Title Here]

        --- Story ---
        [Your Narrative Here]

        Follow these guidelines based on the subject:
        - If the subject is a living being (animal, plant, human): Provide scientific facts about its characteristics, behavior, habitat, and significance in its ecosystem or human culture.
        - If the subject is a non-living object (e.g., an apple, a book, a clock): Narrate its origin, creation process, purpose, historical context, or significance, incorporating real-world facts.
        - If the subject is a landscape or scene: Describe the geological, ecological, or historical context of the location. Include facts about relevant natural phenomena or human activity.
        - If the subject is abstract or unclear: Provide a general historical or scientific context related to the visible elements and form a meaningful, fact-based narrative around them.

        Ensure the response is informative but also engaging, like an educational tale or a mini-documentary script, rather than pure fiction. Stick to verifiable facts where possible.
        """)

        model = genai.GenerativeModel(MODEL_NAME)
        print(f"🤖 Using model: {MODEL_NAME}")

        print("📤 Sending image + prompt to Gemini...")
        # Send the prompt and image to the model
        response = model.generate_content([story_prompt, image])

        # --- Process Response ---
        print("⏳ Processing response from Gemini...")

        # Check for potential safety blocks or empty responses
        if not response.parts:
            print("⚠️ Warning: Model response is empty.")
            feedback = getattr(response, 'prompt_feedback', None)
            if feedback:
                print(f"🚫 Prompt Feedback: {feedback}")
                block_reason = getattr(feedback, 'block_reason', None)
                if block_reason:
                     return f"Story generation failed. Reason: Blocked by API ({block_reason})."
                safety_ratings = getattr(feedback, 'safety_ratings', [])
                if safety_ratings:
                    print("🚨 Safety Ratings:")
                    for rating in safety_ratings: print(f" - {rating.category}: {rating.probability}")
                    return "Story generation failed due to safety concerns detected by the API."

            return "Model did not generate a response. It might be empty or blocked."

        print("✅ Story generated successfully!")
        return response.text # Return the generated text

    except UnidentifiedImageError:
        print("❌ Error: Invalid or unsupported image format.")
        return "Error: Could not identify or open the image data. Please provide a valid image file (e.g., JPEG, PNG)."
    except ImportError:
         print("❌ Error: Required libraries (google-generativeai, Pillow) not installed.")
         return "Error: Missing required libraries. Please install google-generativeai and Pillow."
    except Exception as e:
        # Catch other potential errors (API errors, network issues, etc.)
        print(f"❌ An unexpected error occurred in generate_story: {type(e).__name__}: {str(e)}")
        # Check for common API key errors
        if "API key not valid" in str(e):
             return "Error: Invalid or missing Google API Key. Check your configuration."
        return f"An unexpected error occurred: {str(e)}"
def handle_generate_story():
    # ... (code to get image file)
    if 'image_file' not in request.files:
        return "No image file provided", 400
    file = request.files['image_file']
    if file.filename == '':
        return "No image selected", 400

    try:
        image_data = file.read()
        # Call your function
        story_result = generate_story(image_data) # This might return None

        # *** ADD THIS CHECK ***
        if story_result is None:
            # Handle the case where generate_story returned None
            print("Error in route: generate_story returned None.")
            # You could return a specific error message or render an error template
            return "Sorry, failed to generate story. The content might have been blocked or an API issue occurred.", 500 # Internal Server Error

        # If story_result is NOT None, proceed as before
        # Example: If you were rendering a template
        # return render_template('result.html', story=story_result)

        # Example: If you were returning plain text (ensure it's safe concatenation)
        # final_output = "Generated Story: \n" + story_result # This is now safe
        # return final_output

        # Safest: just return the result if it's expected to be plain text/html
        return story_result

    except Exception as e:
        print(f"Error in /generate_story route: {e}")
        # Log the full error for debugging
        import traceback
        traceback.print_exc()
        return f"An unexpected error occurred in the application: {e}", 500
# --- Example Usage ---
if __name__ == "__main__":
    # Replace with the actual path to your image file
    image_path = "static/sample.png" # <-- CHANGE THIS

    if not os.path.exists(image_path):
        print(f"❌ Error: Example image file not found at '{image_path}'.")
        print("Please update the 'image_path' variable in the script.")
    else:
        try:
            print(f"--- Running Story Generation for: {image_path} ---")
            # Read image file as bytes
            with open(image_path, "rb") as f:
                image_bytes = f.read()

            # Generate the story
            generated_story = generate_story(image_bytes)

            # Print the result
            print("\n" + "="*50)
            print(" ✨ Generated Story ✨")
            print("="*50)
            print(generated_story)
            print("="*50 + "\n")

        except FileNotFoundError:
             # This specific check might be redundant due to the os.path.exists check above,
             # but it's good practice within the try block as well.
            print(f"❌ Error: Could not read the image file at '{image_path}'.")
        except Exception as e:
            print(f"❌ An error occurred during the example execution: {e}")

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

ADMIN_CREDENTIALS = {'email': 'test2@gmail.com', 'password': '000000'}
# Admin dashboard
@app.route('/admin')
def admin_():
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Admin login (handled manually)
        if email == ADMIN_CREDENTIALS['email'] and password == ADMIN_CREDENTIALS['password']:
            session['user'] = 'admin'  # Set session for admin
            return redirect(url_for('admin_'))  # Redirect to admin dashboard

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
    return render_template('profile.html', username=session['user'])# Logout
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(image_file.filename):
        return jsonify({'error': 'Unsupported file format. Please upload a JPG, PNG, or WebP image.'}), 400

    try:
        # You can process the image here if needed
        # For now, we'll just return a success message
        return jsonify({
            'message': 'Image uploaded successfully!',
            'filename': image_file.filename,
            'size': len(image_file.read())
        })

    except Exception as e:
        print("Error uploading image:", e)
        return jsonify({'error': 'Something went wrong while uploading the image.'}), 500
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Image-based story generation
# Assuming db is your Firestore client

# Story saving function (you'll need to fill in the actual implementation)
def save_story_to_file(story_text):
    filename = f"{uuid.uuid4().hex}.txt" # Assuming you have uuid imported
    folder = os.path.join("static", "stories") # Assuming you have os imported
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(story_text)
    return f"/static/stories/{filename}"

# Allowed image formats
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'webp'}

# Dummy function to save the story
def save_story_to_file(story_text):
    filename = f"story_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.txt"
    path = os.path.join("static", "stories", filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(story_text)
    return "/" + path

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

        # ✅ Print story to terminal
        print("Generated Story:\n", story_text)

        # Save the story to a file
        story_path = save_story_to_file(story_text)
        story_url = request.host_url.rstrip('/') + story_path

       # Save story metadata to Firestore
        user_email = session['user']
        
        # Get user document by email
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', user_email).limit(1)
        docs = query.get()
        
        if len(docs) == 1:
            user_id = docs[0].id
            story_data = {
                'url': story_url,
                'text': story_text[:500] + '...',  # Save first 500 chars as preview
                'full_text_path': story_path,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'title': story_text.split('\n')[0] if '\n' in story_text else 'Untitled'
            }
            
            # Add to user's stories subcollection
            db.collection('users').document(user_id).collection('stories').add(story_data)
        else:
            print(f"User with email {user_email} not found")

        return jsonify({
            'story': story_text,
            'story_url': story_url,
            'success': True
             })
        

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Something went wrong while processing the image.'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)