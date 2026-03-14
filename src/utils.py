"""Utility functions for the edge classifier project."""

import logging
import os
import yaml
import random
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


def setup_logging(log_dir: str = "logs", log_level: str = "INFO") -> logging.Logger:
    """
    Configure structured logging with file and console handlers.
    
    Args:
        log_dir: Directory to save log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Configured logger instance
    """
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = Path(log_dir) / f"training_{timestamp}.log"
    
    # Create logger
    logger = logging.getLogger("DarknetClassifier")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        logger.handlers.clear()
    
    # File handler with detailed format
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler with simpler format
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
    
    Returns:
        Configuration dictionary
    
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is malformed
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def set_seed(seed: int = 42):
    """
    Set random seeds for reproducibility.
    
    Args:
        seed: Random seed value
    """
    random.seed(seed)
    np.random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    
    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
    except ImportError:
        pass


def validate_dataframe(
    df: pd.DataFrame, 
    required_columns: list, 
    logger: logging.Logger
) -> bool:
    """
    Validate DataFrame has required columns and basic quality checks.
    
    Args:
        df: Input DataFrame
        required_columns: List of required column names
        logger: Logger instance
    
    Returns:
        True if validation passes, False otherwise
    """
    # Check required columns
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        logger.error(f"Missing required columns: {missing_cols}")
        return False
    
    # Check for empty DataFrame
    if df.empty:
        logger.error("DataFrame is empty")
        return False
    
    # Log basic statistics
    logger.info(f"DataFrame shape: {df.shape}")
    logger.info(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    return True


def get_model_size(model_path: str) -> float:
    """
    Get model file size in MB.
    
    Args:
        model_path: Path to model file
    
    Returns:
        File size in megabytes
    """
    if not os.path.exists(model_path):
        return 0.0
    return os.path.getsize(model_path) / (1024 * 1024)


def create_directories(config: Dict[str, Any]):
    """
    Create necessary project directories.
    
    Args:
        config: Configuration dictionary
    """
    directories = [
        config['output']['model_dir'],
        config['output']['log_dir'],
        'data'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
