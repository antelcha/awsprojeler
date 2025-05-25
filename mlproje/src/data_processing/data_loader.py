"""
Data loading module for house price prediction
"""
import pandas as pd
import numpy as np
from typing import Tuple, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HousingDataLoader:
    """Housing veri seti yükleme ve temel inceleme sınıfı"""
    
    def __init__(self, data_path: str = "data/Housing-1.csv"):
        self.data_path = Path(data_path)
        self.df = None
        self.numeric_columns = None
        self.categorical_columns = None
        
    def load_data(self) -> pd.DataFrame:
        """Veri setini yükle"""
        try:
            logger.info(f"Loading data from {self.data_path}")
            self.df = pd.read_csv(self.data_path)
            logger.info(f"Data loaded successfully. Shape: {self.df.shape}")
            
            # Sütun tiplerini belirle
            self._identify_column_types()
            
            return self.df
            
        except FileNotFoundError:
            logger.error(f"Data file not found: {self.data_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def _identify_column_types(self):
        """Sayısal ve kategorik sütunları belirle"""
        if self.df is not None:
            self.numeric_columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
            self.categorical_columns = self.df.select_dtypes(include=['object']).columns.tolist()
            
            logger.info(f"Numeric columns: {self.numeric_columns}")
            logger.info(f"Categorical columns: {self.categorical_columns}")
    
    def get_basic_info(self) -> dict:
        """Veri seti hakkında temel bilgileri döndür"""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        info = {
            'shape': self.df.shape,
            'columns': self.df.columns.tolist(),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'numeric_columns': self.numeric_columns,
            'categorical_columns': self.categorical_columns,
            'target_column': 'price',
            'memory_usage': self.df.memory_usage(deep=True).sum()
        }
        
        return info
    
    def get_statistical_summary(self) -> dict:
        """İstatistiksel özet bilgiler"""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        summary = {
            'numeric_stats': self.df[self.numeric_columns].describe().to_dict(),
            'categorical_stats': {},
            'missing_percentage': (self.df.isnull().sum() / len(self.df) * 100).to_dict()
        }
        
        # Kategorik değişkenler için özet
        for col in self.categorical_columns:
            summary['categorical_stats'][col] = {
                'unique_count': self.df[col].nunique(),
                'unique_values': self.df[col].unique().tolist(),
                'value_counts': self.df[col].value_counts().to_dict()
            }
        
        return summary
    
    def get_train_test_split_data(self, test_size: float = 0.2, 
                                  random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Train-test split için veriyi ayır"""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        from sklearn.model_selection import train_test_split
        
        train_df, test_df = train_test_split(
            self.df, 
            test_size=test_size, 
            random_state=random_state,
            stratify=None  # Regression problem için stratify kullanmıyoruz
        )
        
        logger.info(f"Train set shape: {train_df.shape}")
        logger.info(f"Test set shape: {test_df.shape}")
        
        return train_df, test_df
    
    def get_X_y(self, target_column: str = 'price') -> Tuple[pd.DataFrame, pd.Series]:
        """Features ve target'ı ayır"""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        X = self.df.drop(columns=[target_column])
        y = self.df[target_column]
        
        logger.info(f"Features shape: {X.shape}")
        logger.info(f"Target shape: {y.shape}")
        
        return X, y


def load_housing_data(data_path: str = "data/Housing-1.csv") -> HousingDataLoader:
    """Factory function to create and load housing data"""
    loader = HousingDataLoader(data_path)
    loader.load_data()
    return loader


if __name__ == "__main__":
    # Test the data loader
    loader = load_housing_data()
    
    # Get basic info
    info = loader.get_basic_info()
    print("=== BASIC INFO ===")
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # Get statistical summary
    stats = loader.get_statistical_summary()
    print("\n=== STATISTICAL SUMMARY ===")
    print("Numeric columns statistics:")
    for col, stat in stats['numeric_stats'].items():
        print(f"{col}: mean={stat['mean']:.2f}, std={stat['std']:.2f}")
    
    print("\nCategorical columns:")
    for col, stat in stats['categorical_stats'].items():
        print(f"{col}: {stat['unique_count']} unique values") 