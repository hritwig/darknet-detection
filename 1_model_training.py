import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from imblearn.over_sampling import SMOTE
import pickle

# 1. DATA INGESTION
print("Loading CIC-Darknet-2020 dataset...")
# Assuming the dataset has been pre-filtered to Benign, Tor, and VPN classes
df = pd.read_csv('data/cic_darknet_2020_filtered.csv')

# 2. DATA PREPROCESSING & CLEANING
print("Cleaning infinite and NaN values...")
# CICFlowMeter often generates 'inf' values for division by zero (e.g., bytes/sec)
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

# Define the optimal minimal feature set for Edge Deployment (Nano Banana)
selected_features = [
    'Flow IAT Max', 
    'Flow IAT Mean', 
    'Fwd Packet Length Std', 
    'Bwd Packet Length Max',
    'Flow Duration',
    'Packet Length Variance'
]

X = df[selected_features]
y = df['target_label'] # Classes: 'Benign', 'VPN', 'Tor'

# Encode target labels to integers for XGBoost
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Scale features for consistent model performance
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# 3. HANDLING CLASS IMBALANCE
print("Applying SMOTE to balance Tor and VPN classes against Benign...")
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_scaled, y_encoded)

# Split into training and testing sets (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled
)

# 4. XGBOOST MODEL CONFIGURATION
print("Configuring XGBoost Classifier for Edge Inference...")
# These parameters would be the output of our Checkpointed Randomized Search
best_params = {
    'max_depth': 7,
    'learning_rate': 0.05,
    'n_estimators': 300,
    'subsample': 0.9,
    'tree_method': 'hist', # Optimized for fast training on tabular data
    'n_jobs': 1 # Constrained to 1 core for safe Nano Banana deployment
}

model = xgb.XGBClassifier(**best_params, objective='multi:softprob', num_class=3)

# 5. MODEL TRAINING
print("Training model...")
model.fit(X_train, y_train)

# 6. MODEL EXPORT (For Nano Banana Deployment)
print("Exporting trained model and scaler...")
with open('models/xgboost_edge_model.pkl', 'wb') as f:
    pickle.dump(model, f)
    
with open('models/feature_scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("Pipeline complete. Model ready for edge deployment.")
