from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.agent import DataInsightAgent
from src.data import DataProcessor
from src.analysis import Analyzer
from src.visualization import Visualizer
from src.report import ReportGenerator
import pandas as pd
import os
import yaml

# 加载配置
with open("config/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 创建FastAPI应用
app = FastAPI(
    title="Auto-Agent API",
    description="自动化数据分析与报告生成智能体",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config["api"]["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化组件
agent = DataInsightAgent()
data_processor = DataProcessor()
analyzer = Analyzer()
visualizer = Visualizer()
report_generator = ReportGenerator()

# 全局变量存储上传的文件
uploaded_files = {}

# 请求模型
class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """与智能体聊天"""
    try:
        response = agent.run(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传数据文件"""
    try:
        # 保存文件
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # 存储文件信息
        file_id = f"file_{len(uploaded_files) + 1}"
        uploaded_files[file_id] = file_path
        
        return {"file_id": file_id, "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
async def analyze_data(file_id: str = Form(...), analysis_type: str = Form(...)):
    """分析数据"""
    try:
        if file_id not in uploaded_files:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        file_path = uploaded_files[file_id]
        
        # 加载数据
        df = data_processor.load_data(file_path)
        
        # 清洗数据
        df = data_processor.clean_data(df)
        
        # 分析数据
        if analysis_type == "descriptive":
            results = analyzer.descriptive_analysis(df)
        elif analysis_type == "time_series":
            # 假设第一个日期列和第一个数值列
            date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if not date_cols or not numeric_cols:
                raise HTTPException(status_code=400, detail="数据中没有日期列或数值列")
            
            results = analyzer.time_series_analysis(df, date_cols[0], numeric_cols[0])
        elif analysis_type == "clustering":
            results = analyzer.clustering_analysis(df)
        else:
            raise HTTPException(status_code=400, detail="不支持的分析类型")
        
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/visualize")
async def visualize_data(file_id: str = Form(...), chart_type: str = Form(...)):
    """可视化数据"""
    try:
        if file_id not in uploaded_files:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        file_path = uploaded_files[file_id]
        
        # 加载数据
        df = data_processor.load_data(file_path)
        
        # 清洗数据
        df = data_processor.clean_data(df)
        
        # 生成图表
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_cols:
            raise HTTPException(status_code=400, detail="数据中没有数值列")
        
        x_col = df.columns[0]
        y_col = numeric_cols[0]
        
        if chart_type == "bar":
            chart_path = visualizer.create_bar_chart(df, x_col, y_col, f"{y_col} 柱状图")
        elif chart_type == "line":
            chart_path = visualizer.create_line_chart(df, x_col, y_col, f"{y_col} 折线图")
        elif chart_type == "scatter":
            if len(numeric_cols) >= 2:
                chart_path = visualizer.create_scatter_chart(df, numeric_cols[0], numeric_cols[1], "散点图")
            else:
                raise HTTPException(status_code=400, detail="数据中至少需要两列数值列")
        elif chart_type == "pie":
            # 选择分类列
            cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            if cat_cols:
                # 计算每个类别的计数
                counts = df[cat_cols[0]].value_counts().reset_index()
                counts.columns = [cat_cols[0], 'count']
                chart_path = visualizer.create_pie_chart(counts, 'count', cat_cols[0], f"{cat_cols[0]} 饼图")
            else:
                raise HTTPException(status_code=400, detail="数据中没有分类列")
        else:
            raise HTTPException(status_code=400, detail="不支持的图表类型")
        
        return {"chart_path": chart_path}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate_report")
async def generate_report(file_id: str = Form(...), report_format: str = Form(...)):
    """生成报告"""
    try:
        if file_id not in uploaded_files:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        file_path = uploaded_files[file_id]
        
        # 加载数据
        df = data_processor.load_data(file_path)
        
        # 清洗数据
        df = data_processor.clean_data(df)
        
        # 分析数据
        analysis_results = analyzer.descriptive_analysis(df)
        
        # 准备报告数据
        report_data = {
            'data_overview': {
                'shape': str(df.shape),
                'columns': list(df.columns),
                'rows': len(df)
            },
            'descriptive_analysis': analysis_results,
            'insights': [
                "数据质量良好，缺失值较少",
                f"{df.columns[0]}列的均值为{df[df.columns[0]].mean():.2f}",
                f"数据集中共有{len(df)}条记录"
            ]
        }
        
        # 生成报告
        if report_format == "html":
            report_path = report_generator.generate_html_report(report_data, "数据分析报告")
        elif report_format == "pdf":
            report_path = report_generator.generate_pdf_report(report_data, "数据分析报告")
        elif report_format == "pptx":
            report_path = report_generator.generate_pptx_report(report_data, "数据分析报告")
        else:
            raise HTTPException(status_code=400, detail="不支持的报告格式")
        
        return {"report_path": report_path}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/{file_id}")
async def get_file(file_id: str):
    """获取文件"""
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    file_path = uploaded_files[file_id]
    return FileResponse(file_path)

@app.get("/api/reports/{report_path:path}")
async def get_report(report_path: str):
    """获取报告"""
    full_path = f"reports/{report_path}"
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="报告不存在")
    
    return FileResponse(full_path)

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

@app.get("/")
async def root():
    """根路径"""
    return {"message": "Auto-Agent API is running. Please use Gradio interface at http://localhost:7860"}
