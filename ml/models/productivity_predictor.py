"""
Productivity Predictor using Prophet for time-series forecasting
Predicts user productivity 24 hours in advance
"""
from prophet import Prophet
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime, timedelta

class ProductivityPredictor:
    """
    Predicts productivity scores using Facebook Prophet
    """
    
    def __init__(self):
        self.model = None
        self.trained = False
        
    def prepare_data(self, df):
        """
        Prepare activity data for Prophet training
        
        Args:
            df: DataFrame with columns [timestamp, productivity_score]
            
        Returns:
            DataFrame with columns [ds, y] required by Prophet
        """
        # Ensure timestamp is datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Prophet requires columns named 'ds' (datetime) and 'y' (value to predict)
        prophet_df = df[['timestamp', 'productivity_score']].copy()
        prophet_df.columns = ['ds', 'y']
        
        # Remove any rows with missing values
        prophet_df = prophet_df.dropna()
        
        # Group by hour and take mean (in case multiple activities per hour)
        prophet_df['ds'] = prophet_df['ds'].dt.floor('H')
        prophet_df = prophet_df.groupby('ds', as_index=False).mean()
        
        # Sort by date
        prophet_df = prophet_df.sort_values('ds').reset_index(drop=True)
        
        print(f"📊 Prepared {len(prophet_df)} hourly data points for training")
        print(f"📅 Date range: {prophet_df['ds'].min()} to {prophet_df['ds'].max()}")
        
        return prophet_df
    
    def train(self, data_path):
        """
        Train the Prophet model on historical activity data
        
        Args:
            data_path: Path to CSV file with activity data
        """
        print(f"🎓 Training Productivity Predictor...")
        print(f"📂 Loading data from: {data_path}")
        
        # Load the data
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file not found: {data_path}")
        
        df = pd.read_csv(data_path)
        print(f"✅ Loaded {len(df)} activities")
        
        # Prepare data for Prophet
        prophet_df = self.prepare_data(df)
        
        # Initialize and configure Prophet
        self.model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=False,
            seasonality_mode='multiplicative',
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10.0
        )
        
        # Train the model
        print("🤖 Training Prophet model...")
        self.model.fit(prophet_df)
        
        self.trained = True
        print("✅ Model training complete!")
        
        return self
    
    def predict(self, periods=24):
        """
        Predict productivity for next N hours
        
        Args:
            periods: Number of hours to predict (default: 24)
            
        Returns:
            DataFrame with predictions including confidence intervals
        """
        if not self.trained or self.model is None:
            raise Exception("Model must be trained before making predictions!")
        
        # Create future dataframe for predictions
        future = self.model.make_future_dataframe(periods=periods, freq='H')
        
        # Make predictions
        forecast = self.model.predict(future)
        
        # Get only the future predictions (not historical)
        predictions = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
        
        # Rename columns for clarity
        predictions.columns = ['timestamp', 'predicted_score', 'lower_bound', 'upper_bound']
        
        # Clip predictions to valid range (0-10)
        predictions['predicted_score'] = predictions['predicted_score'].clip(0, 10)
        predictions['lower_bound'] = predictions['lower_bound'].clip(0, 10)
        predictions['upper_bound'] = predictions['upper_bound'].clip(0, 10)
        
        # Add hour of day for easier reference
        predictions['hour'] = pd.to_datetime(predictions['timestamp']).dt.hour
        
        # Add confidence level
        predictions['confidence'] = 1 - (
            (predictions['upper_bound'] - predictions['lower_bound']) / 10
        )
        predictions['confidence'] = predictions['confidence'].clip(0, 1)
        
        return predictions
    
    def save_model(self, path):
        """
        Save the trained model to disk
        
        Args:
            path: Path where model should be saved
        """
        if not self.trained:
            raise Exception("Cannot save untrained model!")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save the model
        joblib.dump(self.model, path)
        print(f"💾 Model saved to: {path}")
    
    def load_model(self, path):
        """
        Load a trained model from disk
        
        Args:
            path: Path to saved model
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")
        
        self.model = joblib.load(path)
        self.trained = True
        print(f"📂 Model loaded from: {path}")
        
        return self


# Test the model if run directly
if __name__ == "__main__":
    print("="*60)
    print("🤖 Testing Productivity Predictor")
    print("="*60)
    print()
    
    # Initialize predictor
    predictor = ProductivityPredictor()
    
    # Get the correct path to data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ml_dir = os.path.dirname(script_dir)
    data_path = os.path.join(ml_dir, 'data', 'demo_activities.csv')
    
    print(f"📂 Looking for data at: {data_path}")
    
    if not os.path.exists(data_path):
        print("❌ Demo data not found!")
        print("📝 Please run: python scripts/generate_demo_data.py")
        exit(1)
    
    # Train the model
    predictor.train(data_path)
    
    print()
    print("="*60)
    print("🔮 Making 24-hour predictions")
    print("="*60)
    print()
    
    # Make predictions
    predictions = predictor.predict(periods=24)
    
    # Display predictions
    print("📊 Productivity Predictions for Next 24 Hours:")
    print()
    print(predictions.to_string(index=False))
    
    print()
    print("="*60)
    print("📈 Key Insights")
    print("="*60)
    
    # Find peak hours
    peak_hour = predictions.loc[predictions['predicted_score'].idxmax()]
    low_hour = predictions.loc[predictions['predicted_score'].idxmin()]
    
    print(f"🚀 Peak productivity: Hour {int(peak_hour['hour'])}:00 - Score: {peak_hour['predicted_score']:.2f}/10")
    print(f"😴 Lowest productivity: Hour {int(low_hour['hour'])}:00 - Score: {low_hour['predicted_score']:.2f}/10")
    print(f"📊 Average predicted score: {predictions['predicted_score'].mean():.2f}/10")
    print(f"🎯 Average confidence: {predictions['confidence'].mean()*100:.1f}%")
    
    # Save the model
    print()
    model_path = os.path.join(ml_dir, 'saved_models', 'productivity_model.pkl')
    predictor.save_model(model_path)
    
    print()
    print("✅ Productivity Predictor test complete!")
    print()