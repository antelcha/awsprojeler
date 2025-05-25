"""
Data preprocessing module for house price prediction
"""
import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Optional
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import logging

logger = logging.getLogger(__name__)


class HousingDataPreprocessor:
    """Housing veri seti ön işleme sınıfı"""
    
    def __init__(self):
        self.preprocessor = None
        self.target_scaler = None
        self.numeric_columns = None
        self.categorical_columns = None
        self.binary_columns = None
        self.is_fitted = False
        
    def identify_column_types(self, df: pd.DataFrame, target_col: str = 'price') -> Dict[str, List[str]]:
        """Sütun tiplerini belirle"""
        X = df.drop(columns=[target_col])
        
        # Sayısal sütunlar
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        
        # Kategorik sütunlar
        categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
        
        # Binary sütunlar (yes/no gibi)
        binary_cols = []
        multi_categorical_cols = []
        
        for col in categorical_cols:
            unique_values = X[col].unique()
            if len(unique_values) == 2:
                binary_cols.append(col)
            else:
                multi_categorical_cols.append(col)
        
        self.numeric_columns = numeric_cols
        self.binary_columns = binary_cols
        self.categorical_columns = multi_categorical_cols
        
        column_types = {
            'numeric': numeric_cols,
            'binary': binary_cols,
            'categorical': multi_categorical_cols
        }
        
        logger.info(f"Column types identified: {column_types}")
        return column_types
    
    def create_preprocessor(self, df: pd.DataFrame, target_col: str = 'price') -> ColumnTransformer:
        """Preprocessing pipeline oluştur"""
        
        # Sütun tiplerini belirle
        column_types = self.identify_column_types(df, target_col)
        
        # Preprocessing steps
        transformers = []
        
        # Numeric columns: impute + scale
        if self.numeric_columns:
            numeric_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            transformers.append(('num', numeric_transformer, self.numeric_columns))
        
        # Binary columns: label encode
        if self.binary_columns:
            binary_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),
                ('label_encoder', LabelEncoder())
            ])
            transformers.append(('bin', binary_transformer, self.binary_columns))
        
        # Categorical columns: one-hot encode
        if self.categorical_columns:
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),
                ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
            ])
            transformers.append(('cat', categorical_transformer, self.categorical_columns))
        
        # Column transformer
        self.preprocessor = ColumnTransformer(
            transformers=transformers,
            remainder='drop'  # Kalan sütunları at
        )
        
        logger.info("Preprocessor created successfully")
        return self.preprocessor
    
    def fit_transform(self, X: pd.DataFrame, y: pd.Series = None) -> np.ndarray:
        """Preprocessing pipeline'ı fit et ve transform yap"""
        if self.preprocessor is None:
            raise ValueError("Preprocessor not created. Call create_preprocessor() first.")
        
        # Features'ı transform et
        X_transformed = self.preprocessor.fit_transform(X)
        self.is_fitted = True
        
        logger.info(f"Features transformed. Shape: {X_transformed.shape}")
        
        # Target'ı scale et (opsiyonel)
        if y is not None:
            self.target_scaler = StandardScaler()
            y_transformed = self.target_scaler.fit_transform(y.values.reshape(-1, 1)).ravel()
            logger.info("Target variable scaled")
            return X_transformed, y_transformed
        
        return X_transformed
    
    def transform(self, X: pd.DataFrame, y: pd.Series = None) -> np.ndarray:
        """Yeni veriyi transform et"""
        if not self.is_fitted:
            raise ValueError("Preprocessor not fitted. Call fit_transform() first.")
        
        X_transformed = self.preprocessor.transform(X)
        logger.info(f"Features transformed. Shape: {X_transformed.shape}")
        
        if y is not None and self.target_scaler is not None:
            y_transformed = self.target_scaler.transform(y.values.reshape(-1, 1)).ravel()
            return X_transformed, y_transformed
        
        return X_transformed
    
    def inverse_transform_target(self, y_scaled: np.ndarray) -> np.ndarray:
        """Scale edilmiş target değerlerini ters çevir"""
        if self.target_scaler is None:
            logger.warning("Target scaler not fitted. Returning original values.")
            return y_scaled
        
        return self.target_scaler.inverse_transform(y_scaled.reshape(-1, 1)).ravel()
    
    def get_feature_names(self) -> List[str]:
        """Transform edilmiş feature isimlerini al"""
        if not self.is_fitted:
            raise ValueError("Preprocessor not fitted. Call fit_transform() first.")
        
        feature_names = []
        
        # Numeric feature names
        if self.numeric_columns:
            feature_names.extend(self.numeric_columns)
        
        # Binary feature names  
        if self.binary_columns:
            feature_names.extend(self.binary_columns)
        
        # Categorical feature names (one-hot encoded)
        if self.categorical_columns:
            try:
                cat_transformer = self.preprocessor.named_transformers_['cat']
                cat_feature_names = cat_transformer.named_steps['onehot'].get_feature_names_out(self.categorical_columns)
                feature_names.extend(cat_feature_names)
            except:
                # Fallback
                feature_names.extend([f"{col}_encoded" for col in self.categorical_columns])
        
        return feature_names
    
    def get_preprocessing_info(self) -> Dict:
        """Preprocessing bilgilerini döndür"""
        if not self.is_fitted:
            return {"status": "not_fitted"}
        
        info = {
            "status": "fitted",
            "numeric_columns": self.numeric_columns,
            "binary_columns": self.binary_columns, 
            "categorical_columns": self.categorical_columns,
            "total_features_before": sum([
                len(self.numeric_columns) if self.numeric_columns else 0,
                len(self.binary_columns) if self.binary_columns else 0,
                len(self.categorical_columns) if self.categorical_columns else 0
            ]),
            "target_scaled": self.target_scaler is not None
        }
        
        return info


def create_housing_preprocessor(df: pd.DataFrame, target_col: str = 'price') -> HousingDataPreprocessor:
    """Factory function to create housing preprocessor"""
    preprocessor = HousingDataPreprocessor()
    preprocessor.create_preprocessor(df, target_col)
    return preprocessor


if __name__ == "__main__":
    # Test preprocessing
    from data_loader import load_housing_data
    
    # Load data
    loader = load_housing_data()
    X, y = loader.get_X_y()
    
    # Create and test preprocessor
    preprocessor = create_housing_preprocessor(loader.df)
    X_transformed, y_transformed = preprocessor.fit_transform(X, y)
    
    print(f"Original shape: {X.shape}")
    print(f"Transformed shape: {X_transformed.shape}")
    print(f"Feature names: {preprocessor.get_feature_names()}")
    print(f"Preprocessing info: {preprocessor.get_preprocessing_info()}") 