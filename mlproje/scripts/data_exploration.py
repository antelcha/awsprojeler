"""
Housing veri seti keşif scripti
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def explore_housing_data():
    """Housing veri setini incele"""
    
    # Veriyi yükle
    df = pd.read_csv('../data/Housing-1.csv')
    
    print("=" * 50)
    print("HOUSING VERİ SETİ KEŞFİ")
    print("=" * 50)
    
    # Temel bilgiler
    print(f"\n📊 Veri Seti Boyutu: {df.shape}")
    print(f"Satır sayısı: {df.shape[0]}")
    print(f"Sütun sayısı: {df.shape[1]}")
    
    # Sütun isimleri
    print(f"\n📋 Sütunlar:")
    for i, col in enumerate(df.columns):
        print(f"  {i+1}. {col}")
    
    # İlk 5 satır
    print(f"\n🔍 İlk 5 satır:")
    print(df.head())
    
    # Veri tipleri
    print(f"\n📈 Veri Tipleri:")
    print(df.dtypes)
    
    # Eksik değerler
    print(f"\n❌ Eksik Değerler:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("Eksik değer yok!")
    else:
        print(missing[missing > 0])
    
    # Temel istatistikler
    print(f"\n📊 Temel İstatistikler:")
    print(df.describe())
    
    # Kategorik ve sayısal sütunları ayır
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    
    print(f"\n🔢 Sayısal Sütunlar ({len(numeric_columns)}):")
    for col in numeric_columns:
        print(f"  - {col}")
    
    print(f"\n🏷️ Kategorik Sütunlar ({len(categorical_columns)}):")
    for col in categorical_columns:
        print(f"  - {col} (unique: {df[col].nunique()})")
    
    return df, numeric_columns, categorical_columns

if __name__ == "__main__":
    df, numeric_cols, categorical_cols = explore_housing_data() 