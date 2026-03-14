"""Data loading, preprocessing, and feature engineering."""

import logging
import numpy as np
import pandas as pd
from typing import Tuple, Optional
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import pickle
from pathlib import Path


class DataProcessor:
    """Handles all data preprocessing operations."""
    
    def __init__(self, config: dict, logger: logging.Logger):
        """
        Initialize DataProcessor.
        
        Args:
            config: Configuration dictionary
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.label_encoder = LabelEncoder()
        self.scaler = MinMaxScaler()
        self.feature_names = config['data']['selected_features']
        
    def load_data(self) -> pd.DataFrame:
        """
        Load dataset from CSV with error handling.
        
        Returns:
            Loaded DataFrame
        
        Raises:
            FileNotFoundError: If data file doesn't exist
            pd.errors.EmptyDataError: If file is empty
        """
        data_path = self.config['data']['input_path']
        self.logger.info(f"Loading data from: {data_path}")
        
        try:
            df = pd.read_csv(data_path)
            self.logger.info(f"✓ Loaded {len(df):,} records")
            return df
        except FileNotFoundError:
            self.logger.error(f"Data file not found: {data_path}")
            raise
        except pd.errors.EmptyDataError:
            self.logger.error("Data file is empty")
            raise
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean infinite values and NaNs.
        
        Args:
            df: Input DataFrame
        
        Returns:
            Cleaned DataFrame
        """
        initial_rows = len(df)
        
        if self.config['preprocessing']['handle_inf']:
            self.logger.info("Replacing infinite values with NaN...")
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
        
        if self.config['preprocessing']['drop_na']:
            nan_counts = df.isna().sum()
            if nan_counts.any():
                self.logger.warning(f"NaN values found:\n{nan_counts[nan_counts > 0]}")
            
            df.dropna(inplace=True)
            dropped = initial_rows - len(df)
            self.logger.info(f"✓ Dropped {dropped:,} rows ({dropped/initial_rows*100:.2f}%)")
        
        return df
    
    def prepare_features(
        self, 
        df: pd.DataFrame
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract features and target, with validation.
        
        Args:
            df: Input DataFrame
        
        Returns:
            Tuple of (features, encoded_labels)
        
        Raises:
            KeyError: If required columns are missing
        """
        target_col = self.config['data']['target_column']
        
        # Validate columns exist
        missing_features = set(self.feature_names) - set(df.columns)
        if missing_features:
            raise KeyError(f"Missing features: {missing_features}")
        
        if target_col not in df.columns:
            raise KeyError(f"Target column '{target_col}' not found")
        
        # Extract features and target
        X = df[self.feature_names].values
        y = df[target_col].values
        
        # Log class distribution
        unique, counts = np.unique(y, return_counts=True)
        self.logger.info("Class distribution:")
        for label, count in zip(unique, counts):
            self.logger.info(f"  {label}: {count:,} ({count/len(y)*100:.2f}%)")
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        self.logger.info(f"✓ Encoded {len(self.label_encoder.classes_)} classes: "
                        f"{list(self.label_encoder.classes_)}")
        
        return X, y_encoded
    
    def scale_features(
        self, 
        X_train: np.ndarray, 
        X_test: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Scale features using MinMaxScaler.
        
        Args:
            X_train: Training features
            X_test: Test features (optional)
        
        Returns:
            Scaled training (and test) features
        """
        if not self.config['preprocessing']['scale_features']:
            return X_train, X_test
        
        self.logger.info("Scaling features to [0, 1] range...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        if X_test is not None:
            X_test_scaled = self.scaler.transform(X_test)
            return X_train_scaled, X_test_scaled
        
        return X_train_scaled, None
    
    def apply_smote(
        self, 
        X: np.ndarray, 
        y: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply SMOTE for class balancing.
        
        Args:
            X: Input features
            y: Target labels
        
        Returns:
            Resampled features and labels
        """
        if not self.config['preprocessing']['apply_smote']:
            return X, y
        
        self.logger.info("Applying SMOTE for class balancing...")
        
        unique_before, counts_before = np.unique(y, return_counts=True)
        
        smote = SMOTE(
            random_state=self.config['project']['seed'],
            sampling_strategy=self.config['preprocessing']['smote_strategy']
        )
        
        X_resampled, y_resampled = smote.fit_resample(X, y)
        
        unique_after, counts_after = np.unique(y_resampled, return_counts=True)
        
        self.logger.info("SMOTE Results:")
        self.logger.info(f"  Before: {dict(zip(unique_before, counts_before))}")
        self.logger.info(f"  After:  {dict(zip(unique_after, counts_after))}")
        
        return X_resampled, y_resampled
    
    def split_data(
        self, 
        X: np.ndarray, 
        y: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Split data into train and test sets.
        
        Args:
            X: Features
            y: Labels
        
        Returns:
            X_train, X_test, y_train, y_test
        """
        test_size = self.config['data']['test_size']
        seed = self.config['project']['seed']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=test_size, 
            random_state=seed, 
            stratify=y
        )
        
        self.logger.info(f"✓ Train/Test split: {len(X_train):,} / {len(X_test):,}")
        
        return X_train, X_test, y_train, y_test
    
    def save_artifacts(self, output_dir: str):
        """
        Save preprocessing artifacts (scaler, encoder).
        
        Args:
            output_dir: Directory to save artifacts
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        scaler_path = Path(output_dir) / "feature_scaler.pkl"
        encoder_path = Path(output_dir) / "label_encoder.pkl"
        
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        
        self.logger.info(f"✓ Saved preprocessing artifacts to {output_dir}")
