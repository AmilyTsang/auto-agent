import pandas as pd
import numpy as np
from typing import Optional, Dict, Any

class DataProcessor:
    """数据处理类"""
    
    def __init__(self):
        pass
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """加载数据"""
        file_ext = file_path.split('.')[-1].lower()
        
        if file_ext == 'csv':
            return pd.read_csv(file_path)
        elif file_ext == 'xlsx':
            return pd.read_excel(file_path)
        elif file_ext == 'json':
            return pd.read_json(file_path)
        elif file_ext == 'txt':
            return pd.read_csv(file_path, sep='\t')
        else:
            raise ValueError(f"不支持的文件格式: {file_ext}")
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """清洗数据"""
        # 复制数据
        cleaned_df = df.copy()
        
        # 处理缺失值
        for col in cleaned_df.columns:
            if cleaned_df[col].dtype == 'object':
                # 对于分类列，使用众数填充
                cleaned_df[col].fillna(cleaned_df[col].mode()[0], inplace=True)
            else:
                # 对于数值列，使用均值填充
                cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)
        
        # 处理重复值
        cleaned_df.drop_duplicates(inplace=True)
        
        # 处理异常值（使用IQR方法）
        for col in cleaned_df.select_dtypes(include=[np.number]).columns:
            Q1 = cleaned_df[col].quantile(0.25)
            Q3 = cleaned_df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            cleaned_df[col] = np.clip(cleaned_df[col], lower_bound, upper_bound)
        
        return cleaned_df
    
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """转换数据"""
        # 复制数据
        transformed_df = df.copy()
        
        # 转换日期列
        for col in transformed_df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    transformed_df[col] = pd.to_datetime(transformed_df[col])
                except:
                    pass
        
        # 转换分类列
        for col in transformed_df.columns:
            if transformed_df[col].dtype == 'object' and len(transformed_df[col].unique()) < 20:
                transformed_df[col] = transformed_df[col].astype('category')
        
        return transformed_df
    
    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """特征工程"""
        # 复制数据
        engineered_df = df.copy()
        
        # 创建新特征
        # 1. 数值列的统计特征
        numeric_cols = engineered_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            # 添加数值列的和
            engineered_df['numeric_sum'] = engineered_df[numeric_cols].sum(axis=1)
            # 添加数值列的均值
            engineered_df['numeric_mean'] = engineered_df[numeric_cols].mean(axis=1)
        
        # 2. 日期特征
        for col in engineered_df.columns:
            if pd.api.types.is_datetime64_any_dtype(engineered_df[col]):
                engineered_df[f'{col}_year'] = engineered_df[col].dt.year
                engineered_df[f'{col}_month'] = engineered_df[col].dt.month
                engineered_df[f'{col}_day'] = engineered_df[col].dt.day
                engineered_df[f'{col}_weekday'] = engineered_df[col].dt.weekday
        
        return engineered_df
    
    def split_data(self, df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> tuple:
        """分割数据"""
        from sklearn.model_selection import train_test_split
        return train_test_split(df, test_size=test_size, random_state=random_state)
