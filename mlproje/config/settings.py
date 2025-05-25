"""
Project configuration settings
"""
import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # AWS Configuration
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_default_region: str = "us-east-1"
    aws_s3_bucket: str = "house-price-prediction-bucket"
    
    # SageMaker Configuration
    sagemaker_execution_role: Optional[str] = None
    sagemaker_endpoint_name: str = "house-price-endpoint"
    
    # Database Configuration
    database_url: str = "postgresql://user:password@localhost/house_prices"
    redis_url: str = "redis://localhost:6379"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # Model Configuration
    model_name: str = "house_price_model"
    model_version: str = "1.0.0"
    
    # Data Configuration
    dataset_path: str = "data/house_prices.csv"
    feature_store_name: str = "house-features"
    
    # Model parameters
    test_size: float = 0.2
    random_state: int = 42
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings() 