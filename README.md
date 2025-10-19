Rehabit 🎯
An AI-powered productivity tracking and optimization platform that helps users monitor daily activities, analyze productivity patterns, and receive personalized recommendations to improve focus and work habits.
🌟 Features

📊 Activity Tracking: Log work sessions, meetings, exercise, and breaks with productivity scores and focus levels
📈 Real-Time Dashboard: View today's productivity metrics, work time, activity counts, and current streaks
🧠 AI Predictions: Get 24-hour productivity forecasts showing peak performance times
💡 Personalized Recommendations: Receive smart suggestions for timing tasks, taking breaks, and optimizing workflow
📉 Analytics & Insights: Analyze weekly trends, identify most productive hours, and track progress over time
🔥 Streak Tracking: Maintain consistency and build productive habits

🛠️ Tech Stack
Frontend

React - UI framework
Vite - Build tool and dev server
Recharts - Data visualization
Tailwind CSS - Styling
Lucide React - Icons

Backend

Python 3.x - Programming language
FastAPI - Web framework
SQLite - Database
Uvicorn - ASGI server
Pydantic - Data validation

Deployment

Railway - Backend hosting (planned)
ngrok - Development tunneling

📋 Prerequisites

Node.js (v18 or higher)
Python (v3.8 or higher)
npm or yarn
Git

🚀 Getting Started
1. Clone the Repository
bashgit clone https://github.com/harshmakadia19/Rehabit.git
cd Rehabit
2. Backend Setup
bash# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn app.main:app --reload
The backend will be available at http://localhost:8000
API Documentation: Visit http://localhost:8000/docs for interactive Swagger UI
3. Frontend Setup
bash# Navigate to frontend directory (from root)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
The frontend will be available at http://localhost:5173
📁 Project Structure
Rehabit/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application entry point
│   │   ├── models/          # Database models
│   │   ├── routes/          # API endpoints
│   │   └── services/        # Business logic
│   ├── requirements.txt     # Python dependencies
│   └── rehabit.db          # SQLite database
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── App.jsx         # Main app component
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
└── README.md
🔌 API Endpoints
Dashboard

GET /api/dashboard/{user_id} - Get user dashboard data with predictions and recommendations

Activities

POST /api/activities - Log a new activity
GET /api/activities/{user_id} - Get user's activities

Health Check

GET /health - Check API health status

💾 Database Schema
Activities Table

id - Primary key
user_id - User identifier
timestamp - Activity timestamp
activity_type - Type of activity (work, meeting, exercise, break)
duration - Duration in minutes
productivity_score - Score from 0-10
focus_level - Focus level (low, medium, high)
notes - Optional notes

🧪 Testing the Application
Add Test Data
Using Swagger UI (http://localhost:8000/docs):

Navigate to POST /api/activities
Click "Try it out"
Enter test data:

json{
  "user_id": 1,
  "activity_type": "work",
  "duration": 60,
  "productivity_score": 8,
  "focus_level": "high",
  "notes": "Completed project documentation"
}

Click "Execute"

View Dashboard
Navigate to http://localhost:5173/dashboard to see your productivity metrics!
🤝 Team

Ayush Patel - Backend Developer
Diya - Frontend Developer
Harsh Makadia - Project Lead

📝 Development Workflow
Branching Strategy

main - Production-ready code
develop - Development branch
Feature branches - Individual features

Making Changes
bash# Switch to develop branch
git checkout develop

# Pull latest changes
git pull origin develop

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes, then commit
git add .
git commit -m "feat: description of changes"

# Push to develop
git checkout develop
git merge feature/your-feature-name
git push origin develop
🐛 Troubleshooting
Backend Issues
Port 8000 already in use:
bash# Find and kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
Database not found:
The SQLite database will be created automatically on first run.
Frontend Issues
npm not found:
Make sure Node.js is installed and added to PATH. Restart your terminal after installation.
Port 5173 already in use:
Vite will automatically use the next available port.
Network Issues
If working across different networks, use ngrok:
bash# Install ngrok: https://ngrok.com/download
ngrok http 8000

# Update frontend/src/services/api.js with the ngrok URL
const API_BASE_URL = 'https://your-ngrok-url.ngrok-free.app/api';
🔮 Future Enhancements

 Advanced ML models for better predictions
 User authentication and profiles
 Mobile app (React Native)
 Integration with calendar apps
 Export reports (PDF/CSV)
 Team collaboration features
 Dark mode

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

FastAPI documentation
React documentation
Recharts library
Tailwind CSS

📧 Contact
For questions or support, please contact:

GitHub: @harshmakadia19


Made with ❤️ by the Rehabit Team