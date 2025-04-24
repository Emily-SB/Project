# Fabulora - Personalized Stories from Everyday Objects

## Overview
**Fabulora** is a web application that transforms everyday objects into engaging, fact-based narratives using AI-powered image analysis. Users can upload images of objects, scenes, or living beings, and the system generates educational stories with scientific and historical context.

---

## Key Features
- **Image-to-Story Generation**: Uses Google's Gemini AI to analyze images and create narratives  
- **User Authentication**: Firebase-based signup/login system with admin controls  
- **Story Management**: Save and organize generated stories in user profiles   
- **Admin Dashboard**: Monitor user activity and manage content  

---

## Technologies Used
- **Backend**: Flask (Python)  
- **Frontend**: HTML5, CSS3, JavaScript  
- **AI Integration**: Google Gemini API  
- **Database**: Firebase Firestore  
- **Authentication**: Firebase Auth  
- **Styling**: Custom CSS with animations and responsive design  

---

## Installation

### Clone the repository:
```bash
git clone [repository-url]
cd fabulora
```

### Install Python dependencies:
```bash
pip install flask python-dotenv google-generativeai pillow firebase-admin requests
```

### Set up environment variables:
Create a `.env` file in the root directory with the following:
```
GEMINI_API_KEY=your_gemini_api_key
FIREBASE_API_KEY=your_firebase_api_key
```

### Configure Firebase:
- Place your `firebase_config.json` in the project root  
- Initialize Firebase Admin SDK with your credentials  

### Run the application:
```bash
python app.py
```

---

## File Structure
```
fabulora/
├── app.py                 # Main Flask application
├── static/
│   ├── css/               # Stylesheets
│   │   ├── styles.css
│   │   ├── login.css
│   │   └── admin.css
│   └── js/                # JavaScript files
│       ├── script.js
│       ├── login.js
│       └── admin.js
├── templates/             # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── profile.html
│   └── admin.html
├── .env                   # Environment variables
└── firebase_config.json   # Firebase configuration
```

---

## API Endpoints
- `/` - Redirects to login  
- `/login` - User authentication  
- `/signup` - User registration  
- `/profile` - User profile page  
- `/admin` - Admin dashboard  
- `/generate_story` - Image processing and story generation  
- `/logout` - Session termination  

---

## Usage
1. **User Registration**: Sign up with email and password  
2. **Image Upload**: Upload an image through the web interface  
3. **Story Generation**: The system processes the image and displays the generated story  
4. **Story Management**: Save stories to your profile for later access  
5. **Admin Features**: Monitor users and content through the admin dashboard  

---

## Configuration
- Edit `.env` for API keys  
- Modify `firebase_config.json` for Firebase setup  
- Adjust styles in the CSS files for custom branding  

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Future Enhancements
- Social sharing features  
- Multi-language support  
- Advanced story customization options  
- Mobile app development 
- Preview option
- Making the site responsive
- Saving story to backend
- Admin dashboard extension

---