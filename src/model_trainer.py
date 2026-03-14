"""Model training and optimization."""

import logging
import numpy as np
import xgboost as xgb
import pickle
import json
from pathlib import Path
from typing import Dict, Any, Tuple
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, cross_val_score
import time


class ModelTrainer:
    """Handles XGBoost model training and optimization."""
    
    def __init__(self, config: dict, logger: logging.Logger):
        """
        Initialize ModelTrainer.
        
        Args:
            config: Configuration dictionary
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.model = None
        self.best_params = None
        self.training_time = 0
        
    def build_model(self) -> xgb.XGBClassifier:
        """
        Build XGBoost classifier with configured parameters.
        
        Returns:
            Configured XGBoost model
        """
        params = self.config['model']['hyperparameters'].copy()
        
        # Determine number of classes
        params['num_class'] = 3  # Benign, Tor, VPN
        
        self.logger.info("Building XGBoost classifier with parameters:")
        for key, value in params.items():
            self.logger.info(f"  {key}: {value}")
        
        model = xgb.XGBClassifier(**params)
        return model
    
    def hyperparameter_search(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray
    ) -> xgb.XGBClassifier:
        """
        Perform hyperparameter optimization using RandomizedSearchCV.
        
        Args:
            X_train: Training features
            y_train: Training labels
        
        Returns:
            Best model from search
        """
        self.logger.info("Starting hyperparameter search...")
        
        # Define search space
        param_distributions = {
            'max_depth': [3, 5, 7, 9],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'n_estimators': [100, 200, 300, 500],
            'subsample': [0.7, 0.8, 0.9, 1.0],
            'colsample_bytree': [0.7, 0.8, 0.9, 1.0],
            'gamma': [0, 0.1, 0.2, 0.3],
            'min_child_weight': [1, 3, 5]
        }
        
        base_model = xgb.XGBClassifier(
            objective='multi:softprob',
            num_class=3,
            tree_method='hist',
            n_jobs=1,
            random_state=self.config['project']['seed']
        )
        
        search_config = self.config['model']['optimization']
        
        if search_config['search_method'] == 'randomized':
            search = RandomizedSearchCV(
                base_model,
                param_distributions,
                n_iter=search_config['n_iter'],
                cv=search_config['cv_folds'],
                scoring='f1_macro',
                n_jobs=-1,
                random_state=self.config['project']['seed'],
                verbose=2
            )
        else:  # grid search
            search = GridSearchCV(
                base_model,
                param_distributions,
                cv=search_config['cv_folds'],
                scoring='f1_macro',
                n_jobs=-1,
                verbose=2
            )
        
        start_time = time.time()
        search.fit(X_train, y_train)
        search_time = time.time() - start_time
        
        self.best_params = search.best_params_
        self.logger.info(f"✓ Hyperparameter search completed in {search_time:.2f}s")
        self.logger.info(f"Best parameters: {self.best_params}")
        self.logger.info(f"Best CV score: {search.best_score_:.4f}")
        
        return search.best_estimator_
    
    def train(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray,
        X_val: np.ndarray = None,
        y_val: np.ndarray = None
    ) -> xgb.XGBClassifier:
        """
        Train the XGBoost model.
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features (optional)
            y_val: Validation labels (optional)
        
        Returns:
            Trained model
        """
        # Check if hyperparameter search is enabled
        if self.config['model']['optimization']['enable_hyperparameter_search']:
            self.model = self.hyperparameter_search(X_train, y_train)
        else:
            self.model = self.build_model()
        
        self.logger.info("Training XGBoost model...")
        start_time = time.time()
        
        # Prepare evaluation set if validation data provided
        eval_set = [(X_train, y_train)]
        if X_val is not None and y_val is not None:
            eval_set.append((X_val, y_val))
        
        # Train with early stopping if validation set provided
        if len(eval_set) > 1:
            self.model.fit(
                X_train, y_train,
                eval_set=eval_set,
                verbose=False
            )
        else:
            self.model.fit(X_train, y_train)
        
        self.training_time = time.time() - start_time
        self.logger.info(f"✓ Training completed in {self.training_time:.2f}s")
        
        # Cross-validation score
        cv_scores = cross_val_score(
            self.model, X_train, y_train, 
            cv=5, scoring='f1_macro', n_jobs=-1
        )
        self.logger.info(f"Cross-validation F1 (macro): {cv_scores.mean():.4f} "
                        f"(±{cv_scores.std():.4f})")
        
        return self.model
    
    def save_model(self, output_dir: str):
        """
        Save trained model with compression for edge deployment.
        
        Args:
            output_dir: Directory to save model
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Save as pickle (standard)
        model_path = Path(output_dir) / "xgboost_edge_model.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        # Save as JSON (lightweight, portable)
        json_path = Path(output_dir) / "xgboost_edge_model.json"
        self.model.save_model(str(json_path))
        
        # Get model sizes
        pkl_size = model_path.stat().st_size / 1024
        json_size = json_path.stat().st_size / 1024
        
        self.logger.info(f"✓ Model saved:")
        self.logger.info(f"  Pickle: {model_path} ({pkl_size:.2f} KB)")
        self.logger.info(f"  JSON:   {json_path} ({json_size:.2f} KB)")
        
        # Check if model exceeds edge deployment size limit
        max_size_mb = self.config['edge_deployment']['max_model_size_mb']
        if pkl_size / 1024 > max_size_mb:
            self.logger.warning(
                f"⚠ Model size ({pkl_size/1024:.2f} MB) exceeds "
                f"edge deployment limit ({max_size_mb} MB)"
            )
        
        # Save metadata
        metadata = {
            'model_type': 'XGBoostClassifier',
            'version': self.config['project']['version'],
            'training_time_seconds': self.training_time,
            'num_features': len(self.config['data']['selected_features']),
            'feature_names': self.config['data']['selected_features'],
            'num_classes': 3,
            'class_names': ['Benign', 'Tor', 'VPN'],
            'hyperparameters': self.config['model']['hyperparameters'],
            'best_params': self.best_params,
            'model_size_kb': pkl_size
        }
        
        metadata_path = Path(output_dir) / "model_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.logger.info(f"✓ Metadata saved: {metadata_path}")
