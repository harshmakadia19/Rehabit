
# ML Models for Rehabit

## Models

1. **Productivity Predictor** - Time-series forecasting
2. **Pattern Recognition** - Clustering user behavior
3. **Anomaly Detection** - Detect overwork/burnout
4. **Recommendation Engine** - Generate personalized tips

## Setup
```bash
pip install -r requirements.txt
python scripts/generate_demo_data.py
```

## Training Models
```bash
python scripts/train_models.py
```

## Model Files

Trained models saved in `saved_models/`:
- `productivity_model.pkl`
- `pattern_model.pkl`
- `anomaly_model.pkl`
