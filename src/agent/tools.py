from langchain_core.tools import Tool
from langchain_core.pydantic_v1 import BaseModel, Field
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# 全局变量存储数据
data_store = {}
analysis_results = {}

# 数据导入工具
class DataImportInput(BaseModel):
    file_path: str = Field(description="数据文件路径")

def import_data(file_path: str) -> str:
    """导入数据文件并存储到数据存储中"""
    try:
        file_ext = file_path.split('.')[-1].lower()
        
        if file_ext == 'csv':
            df = pd.read_csv(file_path)
        elif file_ext == 'xlsx':
            df = pd.read_excel(file_path)
        elif file_ext == 'json':
            df = pd.read_json(file_path)
        else:
            return f"不支持的文件格式: {file_ext}"
        
        # 生成数据ID
        data_id = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        data_store[data_id] = df
        
        return f"成功导入数据: {data_id}\n数据形状: {df.shape}\n列名: {list(df.columns)}"
    except Exception as e:
        return f"导入数据时出错: {str(e)}"

# 描述性分析工具
class DescriptiveAnalysisInput(BaseModel):
    data_id: str = Field(description="数据ID")

def descriptive_analysis(data_id: str) -> str:
    """对数据进行描述性分析"""
    try:
        if data_id not in data_store:
            return f"数据ID不存在: {data_id}"
        
        df = data_store[data_id]
        
        # 基本统计信息
        stats = df.describe().to_dict()
        
        # 缺失值分析
        missing_values = df.isnull().sum().to_dict()
        
        # 数据类型分析
        dtypes = df.dtypes.astype(str).to_dict()
        
        # 存储分析结果
        analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        analysis_results[analysis_id] = {
            "stats": stats,
            "missing_values": missing_values,
            "dtypes": dtypes
        }
        
        # 生成分析报告
        report = f"描述性分析结果 ({analysis_id}):\n\n"
        report += "基本统计信息:\n"
        for col, stat in stats.items():
            report += f"  {col}:\n"
            for key, value in stat.items():
                report += f"    {key}: {value}\n"
        
        report += "\n缺失值分析:\n"
        for col, count in missing_values.items():
            report += f"  {col}: {count} ({count/len(df)*100:.2f}%)\n"
        
        report += "\n数据类型:\n"
        for col, dtype in dtypes.items():
            report += f"  {col}: {dtype}\n"
        
        return report
    except Exception as e:
        return f"分析数据时出错: {str(e)}"

# 生成图表工具
class GenerateChartInput(BaseModel):
    data_id: str = Field(description="数据ID")
    chart_type: str = Field(description="图表类型: bar, line, scatter, pie")
    title: str = Field(description="图表标题")

def generate_chart(data_id: str, chart_type: str, title: str) -> str:
    """生成数据可视化图表"""
    try:
        if data_id not in data_store:
            return f"数据ID不存在: {data_id}"
        
        df = data_store[data_id]
        
        # 生成图表
        chart_id = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        chart_path = f"outputs/{chart_id}.html"
        
        # 确保输出目录存在
        os.makedirs("outputs", exist_ok=True)
        
        if chart_type == 'bar':
            # 选择数值列
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                fig = px.bar(df, x=df.index, y=numeric_cols[0], title=title)
            else:
                return "数据中没有数值列"
        elif chart_type == 'line':
            # 选择数值列
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                fig = px.line(df, x=df.index, y=numeric_cols[0], title=title)
            else:
                return "数据中没有数值列"
        elif chart_type == 'scatter':
            # 选择数值列
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) >= 2:
                fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=title)
            else:
                return "数据中至少需要两列数值列"
        elif chart_type == 'pie':
            # 选择分类列
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            if len(categorical_cols) > 0:
                # 计算每个类别的计数
                counts = df[categorical_cols[0]].value_counts()
                fig = px.pie(values=counts.values, names=counts.index, title=title)
            else:
                return "数据中没有分类列"
        else:
            return f"不支持的图表类型: {chart_type}"
        
        # 保存图表
        fig.write_html(chart_path)
        
        return f"成功生成图表: {chart_id}\n保存路径: {chart_path}"
    except Exception as e:
        return f"生成图表时出错: {str(e)}"

# 生成报告工具
class GenerateReportInput(BaseModel):
    analysis_id: str = Field(description="分析结果ID")

def generate_report(analysis_id: str) -> str:
    """生成分析报告"""
    try:
        if analysis_id not in analysis_results:
            return f"分析结果ID不存在: {analysis_id}"
        
        # 生成报告
        report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        report_path = f"reports/{report_id}.html"
        
        # 确保报告目录存在
        os.makedirs("reports", exist_ok=True)
        
        # 生成HTML报告
        analysis = analysis_results[analysis_id]
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>数据分析报告</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #555; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>数据分析报告</h1>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>基本统计信息</h2>
            <table>
                <tr>
                    <th>列名</th>
                    <th>计数</th>
                    <th>均值</th>
                    <th>标准差</th>
                    <th>最小值</th>
                    <th>25%</th>
                    <th>50%</th>
                    <th>75%</th>
                    <th>最大值</th>
                </tr>
        """
        
        # 添加统计信息表格
        for col, stat in analysis["stats"].items():
            html_content += f"""
                <tr>
                    <td>{col}</td>
                    <td>{stat.get('count', '')}</td>
                    <td>{stat.get('mean', '')}</td>
                    <td>{stat.get('std', '')}</td>
                    <td>{stat.get('min', '')}</td>
                    <td>{stat.get('25%', '')}</td>
                    <td>{stat.get('50%', '')}</td>
                    <td>{stat.get('75%', '')}</td>
                    <td>{stat.get('max', '')}</td>
                </tr>
            """
        
        html_content += f"""
            </table>
            
            <h2>缺失值分析</h2>
            <table>
                <tr>
                    <th>列名</th>
                    <th>缺失值数量</th>
                </tr>
        """
        
        # 添加缺失值表格
        for col, count in analysis["missing_values"].items():
            html_content += f"""
                <tr>
                    <td>{col}</td>
                    <td>{count}</td>
                </tr>
            """
        
        html_content += f"""
            </table>
            
            <h2>数据类型</h2>
            <table>
                <tr>
                    <th>列名</th>
                    <th>数据类型</th>
                </tr>
        """
        
        # 添加数据类型表格
        for col, dtype in analysis["dtypes"].items():
            html_content += f"""
                <tr>
                    <td>{col}</td>
                    <td>{dtype}</td>
                </tr>
            """
        
        html_content += f"""
            </table>
        </body>
        </html>
        """
        
        # 保存报告
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return f"成功生成报告: {report_id}\n保存路径: {report_path}"
    except Exception as e:
        return f"生成报告时出错: {str(e)}"

# 注册工具
tools = [
    Tool(
        name="数据导入",
        func=import_data,
        description="导入数据文件并存储到数据存储中",
        args_schema=DataImportInput
    ),
    Tool(
        name="描述性分析",
        func=descriptive_analysis,
        description="对数据进行描述性分析",
        args_schema=DescriptiveAnalysisInput
    ),
    Tool(
        name="生成图表",
        func=generate_chart,
        description="生成数据可视化图表",
        args_schema=GenerateChartInput
    ),
    Tool(
        name="生成报告",
        func=generate_report,
        description="生成分析报告",
        args_schema=GenerateReportInput
    )
]

def register_tools():
    """注册工具"""
    return tools
