"""Main training pipeline orchestrator."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.utils import setup_logging, load_config, set_seed, validate_dataframe, create_directories
from src.data_processor import DataProcessor
from src.model_trainer import ModelTrainer
from src.evaluator import ModelEvaluator


def main():
    """Execute the complete training pipeline."""
    
    # Load configuration
    try:
        config = load_config("config/config.yaml")
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return 1
    
    # Setup logging
    logger = setup_logging(
        log_dir=config['output']['log_dir'],
        log_level="INFO"
    )
    
    logger.info("=" * 80)
    logger.info(f"🚀 Starting {config['project']['name']} v{config['project']['version']}")
    logger.info("=" * 80)
    
    # Create necessary directories
    create_directories(config)
    
    # Set random seed for reproducibility
    set_seed(config['project']['seed'])
    logger.info(f"Random seed set to: {config['project']['seed']}")
    
    try:
        # ==================== DATA PROCESSING ====================
        logger.info("\n" + "=" * 80)
        logger.info("STEP 1: DATA PROCESSING")
        logger.info("=" * 80)
        
        data_processor = DataProcessor(config, logger)
        
        # Load data
        df = data_processor.load_data()
        
        # Validate DataFrame
        all_required_cols = (
            config['data']['selected_features'] + 
            [config['data']['target_column']]
        )
        if not validate_dataframe(df, all_required_cols, logger):
            logger.error("Data validation failed")
            return 1
        
        # Clean data
        df = data_processor.clean_data(df)
        
        # Prepare features and labels
        X, y = data_processor.prepare_features(df)
        
        # Split data
        X_train, X_test, y_train, y_test = data_processor.split_data(X, y)
        
        # Scale features
        X_train_scaled, X_test_scaled = data_processor.scale_features(X_train, X_test)
        
        # Apply SMOTE
        X_train_balanced, y_train_balanced = data_processor.apply_smote(
            X_train_scaled, y_train
        )
        
        # Save preprocessing artifacts
        data_processor.save_artifacts(config['output']['model_dir'])
        
        # ==================== MODEL TRAINING ====================
        logger.info("\n" + "=" * 80)
        logger.info("STEP 2: MODEL TRAINING")
        logger.info("=" * 80)
        
        model_trainer = ModelTrainer(config, logger)
        
        # Train model
        model = model_trainer.train(X_train_balanced, y_train_balanced)
        
        # Save model
        model_trainer.save_model(config['output']['model_dir'])
        
        # ==================== MODEL EVALUATION ====================
        logger.info("\n" + "=" * 80)
        logger.info("STEP 3: MODEL EVALUATION")
        logger.info("=" * 80)
        
        evaluator = ModelEvaluator(config, logger)
        
        # Evaluate on test set
        metrics = evaluator.evaluate(
            model, X_test_scaled, y_test, 
            data_processor.label_encoder
        )
        
        # Save metrics
        if config['output']['save_metrics']:
            evaluator.save_metrics(config['output']['model_dir'])
        
        # Plot confusion matrix
        if config['output']['save_confusion_matrix']:
            evaluator.plot_confusion_matrix(
                data_processor.label_encoder,
                config['output']['model_dir']
            )
        
        # Plot feature importance
        if config['output']['save_feature_importance']:
            evaluator.plot_feature_importance(
                model,
                config['data']['selected_features'],
                config['output']['model_dir']
            )
        
        # Estimate edge performance
        evaluator.estimate_edge_performance(model, X_test_scaled)
        
        # ==================== COMPLETION ====================
        logger.info("\n" + "=" * 80)
        logger.info("✅ PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        logger.info(f"Model directory: {config['output']['model_dir']}")
        logger.info(f"Log directory: {config['output']['log_dir']}")
        logger.info(f"Final F1 Score: {metrics['f1_macro']:.4f}")
        
        return 0
        
    except Exception as e:
        logger.exception(f"Pipeline failed with error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
