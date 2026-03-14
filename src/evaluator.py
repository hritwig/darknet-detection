"""Model evaluation and metrics calculation."""

import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, Any
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix, classification_report, roc_auc_score
)
import json


class ModelEvaluator:
    """Handles model evaluation and metric visualization."""
    
    def __init__(self, config: dict, logger: logging.Logger):
        """
        Initialize ModelEvaluator.
        
        Args:
            config: Configuration dictionary
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.metrics = {}
        
    def evaluate(
        self, 
        model, 
        X_test: np.ndarray, 
        y_test: np.ndarray,
        label_encoder
    ) -> Dict[str, Any]:
        """
        Comprehensive model evaluation.
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test labels
            label_encoder: Label encoder for class names
        
        Returns:
            Dictionary of evaluation metrics
        """
        self.logger.info("Evaluating model on test set...")
        
        # Predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)
        
        # Basic metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision, recall, f1, support = precision_recall_fscore_support(
            y_test, y_pred, average='macro'
        )
        
        # Per-class metrics
        precision_per_class, recall_per_class, f1_per_class, support_per_class = \
            precision_recall_fscore_support(y_test, y_pred, average=None)
        
        # ROC AUC (one-vs-rest)
        try:
            roc_auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr', average='macro')
        except Exception as e:
            self.logger.warning(f"Could not calculate ROC AUC: {e}")
            roc_auc = None
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        # Store metrics
        self.metrics = {
            'accuracy': float(accuracy),
            'precision_macro': float(precision),
            'recall_macro': float(recall),
            'f1_macro': float(f1),
            'roc_auc_macro': float(roc_auc) if roc_auc else None,
            'confusion_matrix': cm.tolist(),
            'per_class_metrics': {}
        }
        
        # Per-class metrics with class names
        class_names = label_encoder.classes_
        for i, class_name in enumerate(class_names):
            self.metrics['per_class_metrics'][class_name] = {
                'precision': float(precision_per_class[i]),
                'recall': float(recall_per_class[i]),
                'f1': float(f1_per_class[i]),
                'support': int(support_per_class[i])
            }
        
        # Log results
        self.logger.info("=" * 60)
        self.logger.info("MODEL EVALUATION RESULTS")
        self.logger.info("=" * 60)
        self.logger.info(f"Accuracy:  {accuracy:.4f}")
        self.logger.info(f"Precision: {precision:.4f}")
        self.logger.info(f"Recall:    {recall:.4f}")
        self.logger.info(f"F1 Score:  {f1:.4f}")
        if roc_auc:
            self.logger.info(f"ROC AUC:   {roc_auc:.4f}")
        
        self.logger.info("\nPer-Class Metrics:")
        for class_name, metrics in self.metrics['per_class_metrics'].items():
            self.logger.info(f"\n{class_name}:")
            self.logger.info(f"  Precision: {metrics['precision']:.4f}")
            self.logger.info(f"  Recall:    {metrics['recall']:.4f}")
            self.logger.info(f"  F1:        {metrics['f1']:.4f}")
            self.logger.info(f"  Support:   {metrics['support']}")
        
        self.logger.info("=" * 60)
        
        # Print classification report
        self.logger.info("\nDetailed Classification Report:")
        report = classification_report(y_test, y_pred, target_names=class_names)
        self.logger.info(f"\n{report}")
        
        return self.metrics
    
    def plot_confusion_matrix(
        self, 
        label_encoder, 
        output_dir: str,
        normalize: bool = True
    ):
        """
        Plot and save confusion matrix.
        
        Args:
            label_encoder: Label encoder for class names
            output_dir: Directory to save plot
            normalize: Whether to normalize the confusion matrix
        """
        if 'confusion_matrix' not in self.metrics:
            self.logger.warning("No confusion matrix available to plot")
            return
        
        cm = np.array(self.metrics['confusion_matrix'])
        class_names = label_encoder.classes_
        
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            fmt = '.2f'
            title = 'Normalized Confusion Matrix'
        else:
            fmt = 'd'
            title = 'Confusion Matrix'
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm, 
            annot=True, 
            fmt=fmt, 
            cmap='Blues',
            xticklabels=class_names,
            yticklabels=class_names,
            cbar_kws={'label': 'Count' if not normalize else 'Proportion'}
        )
        plt.title(title, fontsize=16, fontweight='bold')
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.tight_layout()
        
        output_path = Path(output_dir) / "confusion_matrix.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f"✓ Confusion matrix saved: {output_path}")
    
    def plot_feature_importance(
        self, 
        model, 
        feature_names: list,
        output_dir: str,
        top_n: int = None
    ):
        """
        Plot and save feature importance.
        
        Args:
            model: Trained XGBoost model
            feature_names: List of feature names
            output_dir: Directory to save plot
            top_n: Number of top features to display (None for all)
        """
        importance = model.feature_importances_
        
        # Create DataFrame for easier manipulation
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        if top_n:
            importance_df = importance_df.head(top_n)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=importance_df, 
            x='importance', 
            y='feature',
            palette='viridis'
        )
        plt.title('Feature Importance', fontsize=16, fontweight='bold')
        plt.xlabel('Importance Score', fontsize=12)
        plt.ylabel('Feature', fontsize=12)
        plt.tight_layout()
        
        output_path = Path(output_dir) / "feature_importance.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f"✓ Feature importance saved: {output_path}")
        
        # Log top features
        self.logger.info("\nTop Features by Importance:")
        for idx, row in importance_df.iterrows():
            self.logger.info(f"  {row['feature']}: {row['importance']:.4f}")
    
    def save_metrics(self, output_dir: str):
        """
        Save evaluation metrics to JSON file.
        
        Args:
            output_dir: Directory to save metrics
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        metrics_path = Path(output_dir) / "evaluation_metrics.json"
        with open(metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        self.logger.info(f"✓ Metrics saved: {metrics_path}")
    
    def estimate_edge_performance(self, model, X_test: np.ndarray):
        """
        Estimate inference performance on edge device.
        
        Args:
            model: Trained model
            X_test: Test features
        """
        import time
        
        self.logger.info("\nEstimating edge device inference performance...")
        
        # Single sample inference time
        n_samples = min(1000, len(X_test))
        sample = X_test[:1]
        
        times = []
        for _ in range(100):
            start = time.perf_counter()
            _ = model.predict(sample)
            times.append(time.perf_counter() - start)
        
        avg_time_ms = np.mean(times) * 1000
        std_time_ms = np.std(times) * 1000
        
        # Batch inference
        batch_start = time.perf_counter()
        _ = model.predict(X_test[:n_samples])
        batch_time = time.perf_counter() - batch_start
        throughput = n_samples / batch_time
        
        self.logger.info(f"Single sample latency: {avg_time_ms:.3f} ± {std_time_ms:.3f} ms")
        self.logger.info(f"Throughput: {throughput:.1f} samples/sec")
        self.logger.info(f"Expected FPS (real-time): {1000/avg_time_ms:.1f}")
        
        self.metrics['edge_performance'] = {
            'latency_ms': float(avg_time_ms),
            'latency_std_ms': float(std_time_ms),
            'throughput_samples_per_sec': float(throughput)
        }
