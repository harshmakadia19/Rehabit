# Rehabit Backend API

**Developer:** Ayush Patel

## 🚀 Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Run the server
uvicorn app.main:app --reload
```

## 📡 API Endpoints

### Base URL
- Local: `http://localhost:8000`
- Production: TBD

### Endpoints (Building these on Day 2)
- `POST /api/users/create` - Create user
- `POST /api/activities/log` - Log activity
- `GET /api/dashboard/{user_id}` - Get dashboard data
- `GET /api/predictions/{user_id}` - Get ML predictions
- `GET /api/recommendations/{user_id}` - Get AI recommendations

## 📚 Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠️ Tech Stack
- FastAPI (web framework)
- SQLAlchemy (ORM)
- SQLite (database)
- Pydantic (data validation)

## 🔌 ML Integration

Integrates with Harsh's ML models from `../ml/models/`

## ✅ Day 1 Progress
- [x] Backend structure created
- [x] Database models (User, Activity, Prediction)
- [x] Database connection
- [x] Pydantic schemas
- [x] Main FastAPI app with CORS
- [x] Server running successfully