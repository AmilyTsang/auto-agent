import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import os

class Visualizer:
    """数据可视化类"""
    
    def __init__(self, theme: str = "plotly_white"):
        self.theme = theme
        # 确保输出目录存在
        os.makedirs("outputs", exist_ok=True)
    
    def create_bar_chart(self, df: pd.DataFrame, x_col: str, y_col: str, title: str = "Bar Chart") -> str:
        """创建柱状图"""
        fig = px.bar(df, x=x_col, y=y_col, title=title, template=self.theme)
        return self._save_and_return(fig, "bar_chart")
    
    def create_line_chart(self, df: pd.DataFrame, x_col: str, y_col: str, title: str = "Line Chart") -> str:
        """创建折线图"""
        fig = px.line(df, x=x_col, y=y_col, title=title, template=self.theme)
        return self._save_and_return(fig, "line_chart")
    
    def create_scatter_chart(self, df: pd.DataFrame, x_col: str, y_col: str, title: str = "Scatter Chart") -> str:
        """创建散点图"""
        fig = px.scatter(df, x=x_col, y=y_col, title=title, template=self.theme)
        return self._save_and_return(fig, "scatter_chart")
    
    def create_pie_chart(self, df: pd.DataFrame, values_col: str, names_col: str, title: str = "Pie Chart") -> str:
        """创建饼图"""
        fig = px.pie(df, values=values_col, names=names_col, title=title, template=self.theme)
        return self._save_and_return(fig, "pie_chart")
    
    def create_histogram(self, df: pd.DataFrame, x_col: str, title: str = "Histogram") -> str:
        """创建直方图"""
        fig = px.histogram(df, x=x_col, title=title, template=self.theme)
        return self._save_and_return(fig, "histogram")
    
    def create_heatmap(self, df: pd.DataFrame, title: str = "Heatmap") -> str:
        """创建热力图"""
        # 计算相关性矩阵
        numeric_df = df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()
        
        fig = px.imshow(corr_matrix, title=title, template=self.theme)
        return self._save_and_return(fig, "heatmap")
    
    def create_box_plot(self, df: pd.DataFrame, x_col: str, y_col: str, title: str = "Box Plot") -> str:
        """创建箱线图"""
        fig = px.box(df, x=x_col, y=y_col, title=title, template=self.theme)
        return self._save_and_return(fig, "box_plot")
    
    def create_area_chart(self, df: pd.DataFrame, x_col: str, y_col: str, title: str = "Area Chart") -> str:
        """创建面积图"""
        fig = px.area(df, x=x_col, y=y_col, title=title, template=self.theme)
        return self._save_and_return(fig, "area_chart")
    
    def create_3d_scatter(self, df: pd.DataFrame, x_col: str, y_col: str, z_col: str, title: str = "3D Scatter") -> str:
        """创建3D散点图"""
        fig = px.scatter_3d(df, x=x_col, y=y_col, z=z_col, title=title, template=self.theme)
        return self._save_and_return(fig, "3d_scatter")
    
    def create_subplots(self, df: pd.DataFrame, charts: list, title: str = "Subplots") -> str:
        """创建子图"""
        from plotly.subplots import make_subplots
        
        # 计算子图布局
        n_charts = len(charts)
        rows = (n_charts + 1) // 2
        cols = min(2, n_charts)
        
        fig = make_subplots(rows=rows, cols=cols, subplot_titles=[chart['title'] for chart in charts])
        
        # 添加子图
        for i, chart in enumerate(charts, 1):
            row = (i - 1) // cols + 1
            col = (i - 1) % cols + 1
            
            if chart['type'] == 'bar':
                trace = go.Bar(x=df[chart['x']], y=df[chart['y']], name=chart['title'])
            elif chart['type'] == 'line':
                trace = go.Line(x=df[chart['x']], y=df[chart['y']], name=chart['title'])
            elif chart['type'] == 'scatter':
                trace = go.Scatter(x=df[chart['x']], y=df[chart['y']], mode='markers', name=chart['title'])
            
            fig.add_trace(trace, row=row, col=col)
        
        fig.update_layout(title=title, template=self.theme)
        return self._save_and_return(fig, "subplots")
    
    def _save_and_return(self, fig: go.Figure, chart_type: str) -> str:
        """保存图表并返回路径"""
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        chart_id = f"{chart_type}_{timestamp}"
        chart_path = f"outputs/{chart_id}.html"
        
        fig.write_html(chart_path)
        return chart_path
