import pandas as pd
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
from typing import Dict, Any, Optional

class Analyzer:
    """数据分析类"""
    
    def __init__(self):
        pass
    
    def descriptive_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """描述性分析"""
        results = {}
        
        # 基本统计信息
        results['basic_stats'] = df.describe().to_dict()
        
        # 缺失值分析
        results['missing_values'] = df.isnull().sum().to_dict()
        
        # 数据类型分析
        results['data_types'] = df.dtypes.astype(str).to_dict()
        
        # 相关性分析
        numeric_df = df.select_dtypes(include=[np.number])
        if not numeric_df.empty:
            results['correlation'] = numeric_df.corr().to_dict()
        
        return results
    
    def time_series_analysis(self, df: pd.DataFrame, date_col: str, value_col: str) -> Dict[str, Any]:
        """时间序列分析"""
        results = {}
        
        # 确保日期列是 datetime 类型
        df[date_col] = pd.to_datetime(df[date_col])
        df.sort_values(by=date_col, inplace=True)
        
        # 计算趋势
        df['date_num'] = (df[date_col] - df[date_col].min()).dt.days
        X = df['date_num'].values.reshape(-1, 1)
        y = df[value_col].values
        
        model = LinearRegression()
        model.fit(X, y)
        results['trend_slope'] = model.coef_[0]
        results['trend_intercept'] = model.intercept_
        results['trend_r2'] = r2_score(y, model.predict(X))
        
        # 计算季节性
        df['month'] = df[date_col].dt.month
        monthly_avg = df.groupby('month')[value_col].mean()
        results['seasonal_pattern'] = monthly_avg.to_dict()
        
        # 计算移动平均
        df['moving_avg_7'] = df[value_col].rolling(window=7).mean()
        df['moving_avg_30'] = df[value_col].rolling(window=30).mean()
        
        results['moving_avg'] = {
            '7_day': df['moving_avg_7'].dropna().to_dict(),
            '30_day': df['moving_avg_30'].dropna().to_dict()
        }
        
        return results
    
    def clustering_analysis(self, df: pd.DataFrame, n_clusters: int = 3) -> Dict[str, Any]:
        """聚类分析"""
        results = {}
        
        # 选择数值列
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            return {"error": "没有数值列可用于聚类分析"}
        
        # 标准化数据
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_df)
        
        # 执行K-means聚类
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(scaled_data)
        
        # 计算每个聚类的中心
        cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
        results['cluster_centers'] = {}
        for i, center in enumerate(cluster_centers):
            results['cluster_centers'][f'cluster_{i}'] = dict(zip(numeric_df.columns, center))
        
        # 计算每个聚类的大小
        cluster_sizes = pd.Series(clusters).value_counts().to_dict()
        results['cluster_sizes'] = cluster_sizes
        
        # 计算每个聚类的统计信息
        df['cluster'] = clusters
        cluster_stats = {}
        for i in range(n_clusters):
            cluster_data = df[df['cluster'] == i]
            cluster_stats[f'cluster_{i}'] = cluster_data.select_dtypes(include=[np.number]).describe().to_dict()
        results['cluster_stats'] = cluster_stats
        
        return results
    
    def regression_analysis(self, df: pd.DataFrame, target_col: str, feature_cols: list) -> Dict[str, Any]:
        """回归分析"""
        results = {}
        
        # 准备数据
        X = df[feature_cols]
        y = df[target_col]
        
        # 添加常数项
        X = sm.add_constant(X)
        
        # 拟合线性回归模型
        model = sm.OLS(y, X)
        results_ols = model.fit()
        
        # 提取结果
        results['coefficients'] = results_ols.params.to_dict()
        results['r_squared'] = results_ols.rsquared
        results['adjusted_r_squared'] = results_ols.rsquared_adj
        results['f_statistic'] = results_ols.fvalue
        results['p_value'] = results_ols.f_pvalue
        results['summary'] = results_ols.summary().as_text()
        
        return results
    
    def hypothesis_testing(self, df: pd.DataFrame, group_col: str, value_col: str) -> Dict[str, Any]:
        """假设检验"""
        results = {}
        
        # 分组数据
        groups = []
        for group in df[group_col].unique():
            group_data = df[df[group_col] == group][value_col].dropna()
            if len(group_data) > 0:
                groups.append(group_data)
        
        if len(groups) < 2:
            return {"error": "至少需要两组数据进行假设检验"}
        
        # 方差齐性检验
        stat, p_value = stats.levene(*groups)
        results['levene_test'] = {
            'statistic': stat,
            'p_value': p_value,
            'homogeneity': p_value > 0.05
        }
        
        # 方差分析
        if len(groups) > 2:
            stat, p_value = stats.f_oneway(*groups)
            results['anova'] = {
                'statistic': stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        else:
            # t检验
            stat, p_value = stats.ttest_ind(groups[0], groups[1], equal_var=results['levene_test']['homogeneity'])
            results['t_test'] = {
                'statistic': stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        
        return results
