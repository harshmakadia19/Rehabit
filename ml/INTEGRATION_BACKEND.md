
# ML Models Integration Guide for Backend

**Author:** Harsh Makadia  
**For:** Ayush (Backend Team)

## 🎯 Overview

This guide shows you how to integrate the ML models into your FastAPI backend.

---

## 📦 **What ML Provides**

The ML system provides 4 trained models that can:
1. **Predict productivity** for next 24 hours
2. **Identify user patterns** (Morning Person, Night Owl, etc.)
3. **Detect anomalies** (burnout risk, overwork)
4. **Generate recommendations** (personalized tips)

---

## 🗂️ **ML File Structure**

```
ml/
├── models/
│   ├── productivity_predictor.py    # Prophet model
│   ├── pattern_recognition.py       # K-Means clustering
│   ├── anomaly_detection.py         # Isolation Forest
│   └── recommendation_engine.py     # Recommendation logic
├── saved_models/
│   ├── productivity_model.pkl       # Trained Prophet model
│   ├── pattern_model.pkl            # Trained K-Means model
│   └── anomaly_model.pkl            # Trained Isolation Forest
├── data/
│   └── demo_activities.csv          # Sample training data
└── sample_output.json               # Example API response format
```
