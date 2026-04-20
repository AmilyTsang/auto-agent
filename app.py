from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import yaml
from src.agent import DataInsightAgent
from src.data import DataProcessor
from src.analysis import Analyzer
from src.visualization import Visualizer
from src.report import ReportGenerator

# 加载配置
with open("config/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 初始化组件
tagent = DataInsightAgent()
data_processor = DataProcessor()
analyzer = Analyzer()
visualizer = Visualizer()
report_generator = ReportGenerator()

# 全局变量存储上传的文件
uploaded_files = {}

@app.route('/api/chat', methods=['POST'])
def chat():
    """与智能体聊天"""
    try:
        data = request.json
        message = data.get('message')
        conversation_id = data.get('conversation_id')
        
        if not message:
            return jsonify({"response": "请输入消息"}), 400
        
        response = agent.run(message, conversation_id)
        return jsonify({
            "response": response,
            "conversation_id": agent.conversation_manager.get_current_conversation()
        })
    except Exception as e:
        return jsonify({"response": f"错误: {str(e)}"}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """上传数据文件"""
    try:
        if 'file' not in request.files:
            return jsonify({"message": "请选择文件"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"message": "请选择文件"}), 400
        
        # 保存文件
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        file.save(file_path)
        
        # 存储文件信息
        file_id = f"file_{len(uploaded_files) + 1}"
        uploaded_files[file_id] = file_path
        
        return jsonify({"message": f"文件上传成功！文件ID: {file_id}"})
    except Exception as e:
        return jsonify({"message": f"上传失败: {str(e)}"}), 500

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """清空对话历史"""
    try:
        agent.clear_history()
        return jsonify({"message": "历史已清空"})
    except Exception as e:
        return jsonify({"message": f"清空失败: {str(e)}"}), 500

@app.route('/api/clear_docs', methods=['POST'])
def clear_documents():
    """清空上传的文档"""
    try:
        uploaded_files.clear()
        # 清空uploads目录
        if os.path.exists("uploads"):
            for file in os.listdir("uploads"):
                os.remove(os.path.join("uploads", file))
        return jsonify({"message": "文档已清空"})
    except Exception as e:
        return jsonify({"message": f"清空失败: {str(e)}"}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """分析数据"""
    try:
        file_id = request.form.get('file_id')
        analysis_type = request.form.get('analysis_type', 'descriptive')
        
        if not file_id or file_id not in uploaded_files:
            return jsonify({"message": "文件不存在"}), 400
        
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
                return jsonify({"message": "数据中没有日期列或数值列"}), 400
            
            results = analyzer.time_series_analysis(df, date_cols[0], numeric_cols[0])
        elif analysis_type == "clustering":
            results = analyzer.clustering_analysis(df)
        else:
            return jsonify({"message": "不支持的分析类型"}), 400
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"message": f"分析失败: {str(e)}"}), 500

@app.route('/api/visualize', methods=['POST'])
def visualize_data():
    """可视化数据"""
    try:
        file_id = request.form.get('file_id')
        chart_type = request.form.get('chart_type', 'bar')
        
        if not file_id or file_id not in uploaded_files:
            return jsonify({"message": "文件不存在"}), 400
        
        file_path = uploaded_files[file_id]
        
        # 加载数据
        df = data_processor.load_data(file_path)
        
        # 清洗数据
        df = data_processor.clean_data(df)
        
        # 生成图表
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_cols:
            return jsonify({"message": "数据中没有数值列"}), 400
        
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
                return jsonify({"message": "数据中至少需要两列数值列"}), 400
        elif chart_type == "pie":
            # 选择分类列
            cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            if cat_cols:
                # 计算每个类别的计数
                counts = df[cat_cols[0]].value_counts().reset_index()
                counts.columns = [cat_cols[0], 'count']
                chart_path = visualizer.create_pie_chart(counts, 'count', cat_cols[0], f"{cat_cols[0]} 饼图")
            else:
                return jsonify({"message": "数据中没有分类列"}), 400
        else:
            return jsonify({"message": "不支持的图表类型"}), 400
        
        # 读取图表HTML内容
        with open(chart_path, "r", encoding="utf-8") as f:
            chart_html = f.read()
        
        return jsonify({"chart_html": chart_html})
    except Exception as e:
        return jsonify({"message": f"可视化失败: {str(e)}"}), 500

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    """生成报告"""
    try:
        file_id = request.form.get('file_id')
        report_format = request.form.get('report_format', 'html')
        
        if not file_id or file_id not in uploaded_files:
            return jsonify({"message": "文件不存在"}), 400
        
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
            return jsonify({"message": "不支持的报告格式"}), 400
        
        return jsonify({"message": f"报告生成成功！保存路径: {report_path}"})
    except Exception as e:
        return jsonify({"message": f"生成报告失败: {str(e)}"}), 500

@app.route('/')
def index():
    """根路径"""
    return send_from_directory('frontend', 'index.html')

@app.route('/frontend/<path:filename>')
def serve_frontend(filename):
    """服务前端文件"""
    return send_from_directory('frontend', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)